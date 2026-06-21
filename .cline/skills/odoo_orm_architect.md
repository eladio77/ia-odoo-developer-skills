---
name: architecting-odoo-orm
description: |
  Designs, optimizes, and debugs Odoo backend models and ORM logic for v16.0 to v19.0. Use this skill when the user asks to write computed fields, custom database constraints, execute safe raw SQL, or optimize database queries to avoid the N+1 problem.
  Do NOT use for writing external RPC client scripts, building frontend JS/OWL widgets, or creating deployment manifests.
version: 4.0.0
license: MIT
allowed-tools:
  - Read
  - Write
metadata:
  author: CTiEG
  email: hola@ctieg.com
  website: www.ctieg.com
---

# Architecting Odoo Odoo ORM

## When to use
* **Computed Fields & Business Logic**: Implementing computed fields (stored or on-the-fly), onchanges, and data validators on Odoo models.
* **ORM Query Optimization**: Rewriting loop queries, leveraging prefetching, and using `_read_group` to prevent the N+1 query problem.
* **Transactional Controls**: Managing explicit savepoints (`env.cr.savepoint()`) or handling advanced cache flush and invalidations cleanly.
* **Safe Raw SQL Execution**: Running optimized SQL queries with Odoo 19's `env.execute_query` or compiling queries safely using the `odoo.tools.SQL` object.

## When NOT to use
* **External Integrations**: Writing scripts using XML-RPC or JSON-RPC to access Odoo remotely.
* **Theme & UI Layouts**: Creating actions, menus, form views, list views, or reports.
* **Web Client & Frontend**: Developing OWL JS widgets, controllers, or assets.

## Workflow
1. **Ensure Recordset-Level Design (Avoid N+1)**:
   * Odoo uses an automatic prefetching mechanism. When iterating over a recordset, Odoo keeps track of the remaining records and fetches the requested field for *all* records in a single query.
   * **Never** instantiate or browse records individually inside Python loops (e.g., `self.env['model'].browse(id)`), as this breaks prefetching and forces $\mathcal{O}(N)$ database calls.
   * When modifying fields, write in bulk directly to the recordset (e.g., `records.write({'state': 'draft'})`) rather than calling `.write` on single records within a loop.
2. **Aggregations in PostgreSQL**:
   * Do not loop over records in Python to compute averages, sums, or minimums/maximums.
   * Leverage the native ORM method `_read_group` (which replaces the deprecated `read_group` in Odoo 18+) to run `GROUP BY` aggregates directly in PostgreSQL.
3. **Execute SQL Safely (Odoo 17 & 19 Standards)**:
   * **Never** pass unescaped variables or raw strings to `self.env.cr.execute()`, which opens critical SQL injection vulnerabilities.
   * Use Odoo 17's **`odoo.tools.SQL`** composable wrapper to build safe, injection-proof SQL queries.
   * For Odoo 19+, use **`self.env.execute_query(SQL)`** as a safer, cache-aware alternative to direct database cursors.
4. **Cache and Transaction Governance**:
   * Always pair raw SQL execution (`INSERT`, `UPDATE`, `DELETE`) with proper Odoo cache operations:
     * Flush pending calculations first using `model.flush_model(fnames)` or `recordset.flush_recordset(fnames)`.
     * Execute SQL query.
     * Invalidate modified caches using `model.invalidate_model(fnames)` or `recordset.invalidate_recordset(fnames)`.
     * Inform dependent calculated fields of changes by calling `recordset.modified(fnames)`.
   * To prevent database-level crashes during batch loops, isolate operations using savepoints: `with self.env.cr.savepoint():`. Limiting savepoints to fewer than 64 per transaction avoids severe PostgreSQL degradation.
5. **Acknowledge Odoo 19 Deprecations**:
   * The namespace `odoo.osv` is fully deprecated.
   * Directly accessing `record._cr`, `record._context`, and `record._uid` is deprecated. Use `record.env.cr`, `record.env.context`, and `record.env.uid` instead.
   * The `read_group` method is deprecated for backend use. Implement `_read_group` instead.
6. **Master Odoo 19 Search Operators**:
   * Use the **`any!`** operator in search domains to match related records while bypassing access rights validation.
   * Leverage Odoo 19's native support for dynamic relative dates in XML search views and domains (e.g., `today -7d`, `now +2h`).

## Examples

### Example 1: Full-Featured, High-Performance Odoo 19 Model
```python
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import SQL

class ProjectTaskOptimizer(models.Model):
    _name = "project.task.optimizer"
    _description = "Advanced Task Optimizer"
    _order = "sequence, id desc"
    _check_company_auto = True

    name = fields.Char(string="Title", required=True)
    sequence = fields.Integer(string="Sequence", default=10)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'In Progress'),
        ('done', 'Completed')
    ], string="State", default="draft", required=True)
    
    company_id = fields.Many2one(
        'res.company', string="Company", 
        default=lambda self: self.env.company, required=True
    )
    
    # Secure relational field with multi-company auto-checks
    partner_id = fields.Many2one(
        'res.partner', string="Client", 
        check_company=True, index="btree"
    )
    
    estimated_hours = fields.Float(string="Estimated Hours")
    discount_rate = fields.Float(string="Discount Rate", default=0.0)
    
    # Stored computed field optimized for quick retrieval and UI display
    cost_total = fields.Monetary(
        compute="_compute_cost_total", 
        currency_field="currency_id", 
        store=True,
        precompute=True
    )
    
    currency_id = fields.Many2one(
        'res.currency', related="company_id.currency_id", store=True
    )

    # 1. Modern name display compute (replacing deprecated name_get())
    @api.depends('name', 'state')
    def _compute_display_name(self):
        for record in self:
            state_label = dict(self._fields['state'].selection(self)).get(record.state, '')
            record.display_name = f"[{state_label.upper()}] {record.name}"

    # 2. Optimized stored compute with precise dependencies
    @api.depends('estimated_hours', 'discount_rate')
    def _compute_cost_total(self):
        for record in self:
            base_rate = 50.0
            net_rate = base_rate * (1.0 - (record.discount_rate / 100.0))
            record.cost_total = record.estimated_hours * net_rate

    # 3. Model validation constraints (Only supports simple field paths)
    @api.constrains('estimated_hours', 'discount_rate')
    def _check_task_values(self):
        for record in self:
            if record.estimated_hours <= 0:
                raise ValidationError(_("Estimated hours must be a strictly positive value."))
            if not (0.0 <= record.discount_rate <= 100.0):
                raise ValidationError(_("Discount rate must be between 0% and 100%."))

    # 4. Multi-record creation optimization (Mandatory decorator)
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = _("Untitled Task")
        return super(ProjectTaskOptimizer, self).create(vals_list)

    # 5. Safe validation before deletion
    @api.ondelete(at_uninstall=False)
    def _prevent_done_deletion(self):
        for record in self:
            if record.state == 'done':
                raise ValidationError(_("You cannot delete a task in 'Completed' state."))

    # 6. Advanced SQL query using safe Odoo 19 execute_query
    def action_bulk_cost_update(self, multiplier):
        self.ensure_one()
        # Create a safe composable SQL object with automatic table prefixing
        query = SQL(
            "UPDATE %s SET estimated_hours = estimated_hours * %s WHERE id = %s",
            SQL.identifier(self._table),
            multiplier,
            self.id
        )
        
        # Flush the estimated_hours field cache before executing database writes
        self.flush_recordset(['estimated_hours'])
        
        # Execute query cleanly
        self.env.execute_query(query)
        
        # Invalidate the cache to force recalculation on next access
        self.invalidate_recordset(['estimated_hours'])
        
        # Alert downstream computed fields of changes
        self.modified(['estimated_hours'])
```

## Output format
ORM designs produced by this skill must:
* Be structured as standard, PEP8-compliant Python model classes inheriting from `models.Model`, `models.TransientModel`, or `models.AbstractModel`.
* Define computed methods as private (beginning with an underscore `_`) and decorate them with `@api.depends(...)`.
* Avoid standard SQL injection vulnerabilities by compiling queries cleanly using `odoo.tools.SQL`.
* Minimize database transactions by leveraging batch operations.

## Anti-patterns to avoid
* **DO NOT** call `self.env.cr.commit()` or `self.env.cr.rollback()` manually unless you explicitly initialized a separate database cursor. Manual commits bypass test rollbacks, cause data desynchronization, and pollute the database.
* **DO NOT** access `self._cr` or `self._context` directly. Use `self.env.cr` and `self.env.context` instead to satisfy Odoo 19 requirements.
* **DO NOT** write `@api.onchange` decorators for backend business logic. Onchanges are UI-only and are completely bypassed during programmatic creations or writes. Use `@api.depends` instead.
* **DO NOT** execute search operations inside loops. Always perform search outside and map/prefetch records.
* **DO NOT** use `read_group` in backend code. Implement `_read_group` to remain compatible with Odoo 18/19.
