# Skill: Odoo ORM Architecture & Query Optimization Specialist

This Skill equips the Cline agent with high-level database engineering rules, cache management, and structural migration patterns from Odoo v16.0 to v19.0+.

---

## ⚡ Performance Framework & N+1 Prevention
Odoo's ORM maps Python models to PostgreSQL. Poor coding patterns lead to critical latency bottlenecks.
* **Cache & Prefetching:** Odoo leverages automatic record prefetching [540]. When iterating through a recordset (e.g., from a `search()`), Odoo stores all record IDs in a cache [540]. Accessing a field on the first record triggers a single bulk SQL query to fetch values for *all* records in the prefetch set [540, 541].
* **The Loop Antipatron:** Never call `search()` or `browse()` inside loops [432]. Doing so breaks the prefetching mechanism and triggers $N+1$ SQL queries [431, 432].
* **Disabling Prefetching:** If you must read individual records and wish to prevent bulk cache population, call `with_prefetch()` on the recordset with a customized prefetch ID set or `False` [954].
* **Database Agregations:** Do not run mathematical loops (e.g., sum, avg) on Python recordsets [554]. Instead, use the native `_read_group()` method to push aggregation computations down to PostgreSQL using standard SQL aggregators (`SUM`, `AVG`, `COUNT`) [554, 585].

---

## 🛡 SQL Composition & Safe Execution
Odoo 19 introduces strict standards for executing custom SQL commands safely without bypassing ORM intelligence.
* **Do Not Use `cr.execute()` directly:** Standard raw cursor execution is not cache-aware and exposes Odoo to SQL injection [58, 562].
* **Safe Helper:** Use the Odoo 19 `self.env.execute_query(query: odoo.tools.sql.SQL)` helper [558]. It automatically parses the query metadata, flushes pending database changes for affected fields, executes the SQL, and returns a list of tuples [558].
* **The SQL Composition Object:** Always wrap queries in the `odoo.tools.SQL` class (introduced in v17) [116, 562]. This class is composable, maps parameters securely, and prevents SQL injection [563]:
  ```python
  from odoo.tools import SQL
  
  # Composable and safe query definition
  query = SQL("SELECT name FROM res_partner WHERE country_id = %s", country_id)
  results = self.env.execute_query(query)
  ```
  *Note:* The percent character `%` must always be escaped as `%%` within the `SQL` helper (e.g., `SQL("name LIKE 'a%%'")`) [562].

---

## 💾 Caching, Flushing, & Cache Invalidation
When running low-level SQL writes (`UPDATE`/`DELETE`), the ORM's cache can become desynchronized [567]. Apply strict and specific flushing and invalidation routines [117, 567]:
* **Specific Flushing:** Avoid calling `env.flush_all()` unless absolutely necessary, as it flushes everything in memory, delaying execution [565]. Instead, use focused flushing APIs:
  * `self.env['model.name'].flush_model(fnames=None)`: Flushes only pending computations of specific fields of a model to the database [565, 566].
  * `recordset.flush_recordset(fnames=None)`: Flushes specific fields for specific records [566].
* **Specific Cache Invalidation:** If you modify database values directly via SQL, invalidate Odoo's cache to prevent stale reads:
  * `self.env['model.name'].invalidate_model(fnames=None, flush=True)`: Invalidates specific fields of all records of a model in the cache [568].
  * `recordset.invalidate_recordset(fnames=None, flush=True)`: Invalidates cache for a specific record subset [569].
* **Recomputation Trigger:** After direct SQL updates, you must notify Odoo which computed fields depend on those changes by calling the `modified()` method:
  * `recordset.modified(fnames)`: Flags modifications, invalidates the cache, and schedules recomputations of dependent stored fields [571, 572].

---

## ⛔ Modern Decorators & v19 API Changes
Avoid legacy Odoo practices. Enforce compliance with Odoo 19 structures:

* **Deprecated attributes in v19:** Accessing `record._cr`, `record._context`, and `record._uid` is deprecated [111]. Use `record.env.cr`, `record.env.context`, and `record.env.user.id` instead [111, 533].
* **`read_group` Deprecation:** The classic `read_group` is deprecated [113]. Use `_read_group()` for backend calculations [113, 585].
* **`@api.private`:** Restricts public Python methods from being exposed via XML-RPC/JSON-RPC, protecting sensitive internal functions from unauthorized remote calls [113, 551].
* **`@api.model_create_multi`:** Mandatorily decorates any override of `create()`. Accepts a list of dictionaries (`vals_list`) to enable bulk Postgres insertions instead of sequential operations [6, 17, 1010].
* **`@api.ondelete(at_uninstall=False)`:** Handles delete (`unlink()`) restrictions [897]. Setting `at_uninstall=False` ensures modules can still be cleanly uninstalled without custom restrictions blocking database deletion [549, 550, 897].
* **`any!` relation operator:** The dynamic date operators and the relationship operators inside search domains are updated:
  * Use `any!` (e.g., `[('order_line', 'any!', [('product_id', '=', out_of_stock_id)])]`) to execute nested checks while bypassing record rules or access restrictions [588].
  * Domains natively accept relative date terminology (e.g., `[('date_order', '>=', 'today -7d')]`) [111, 592].

---

## 📄 Odoo 19 Optimized Backend Model Reference

```python
# -*- coding: utf-8 -*-
# Copyright 2026 CTiEG - hola@ctieg.com - www.ctieg.com
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import SQL

class TaskOptimizer(models.Model):
    _name = "ctieg.task.optimizer"
    _description = "Advanced CTiEG Task Optimizer"
    _order = "sequence, id desc"
    _check_company_auto = True  # Enforces multi-company record safety automatically

    name = fields.Char(string="Task Title", required=True)
    sequence = fields.Integer(string="Sequence", default=10)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'In Progress'),
        ('done', 'Done')
    ], string="State", default='draft', required=True)
    
    # Active field activates archive/unarchive routines safely
    active = fields.Boolean(default=True)

    company_id = fields.Many2one(
        'res.company', string="Company",
        default=lambda self: self.env.company, required=True
    )
    
    partner_id = fields.Many2one(
        'res.partner', string="Customer",
        check_company=True, index="btree"  # Multi-company validation and database indexing
    )
    
    estimated_hours = fields.Float(string="Estimated Hours")
    discount_rate = fields.Float(string="Discount Rate", default=0.0)
    
    # Stored computed fields optimize reads and search filters
    cost_total = fields.Monetary(
        compute="_compute_cost_total",
        currency_field="currency_id",
        store=True
    )
    
    currency_id = fields.Many2one(
        'res.currency', related="company_id.currency_id", store=True
    )

    # 1. Odoo 18/19 display name standard (name_get is extinct)
    @api.depends('name', 'state')
    def _compute_display_name(self):
        for record in self:
            state_label = dict(self._fields['state'].selection(self)).get(record.state, '')
            record.display_name = f"[{state_label.upper()}] {record.name}"

    # 2. Optimized calculation with tight dependencies
    @api.depends('estimated_hours', 'discount_rate')
    def _compute_cost_total(self):
        for record in self:
            base_rate = 75.0
            net_rate = base_rate * (1.0 - (record.discount_rate / 100.0))
            record.cost_total = record.estimated_hours * net_rate

    # 3. Database constraints checker
    @api.constrains('estimated_hours', 'discount_rate')
    def _check_values(self):
        for record in self:
            if record.estimated_hours <= 0:
                raise ValidationError(_("Estimated hours must be strictly positive."))
            if not (0.0 <= record.discount_rate <= 100.0):
                raise ValidationError(_("Discount rate must be comprised between 0% and 100%."))

    # 4. Mandatory Create Multi (Batch Creation)
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = _("New Scheduled Task")
        return super(TaskOptimizer, self).create(vals_list)

    # 5. Delete protection matching OCA standards
    @api.ondelete(at_uninstall=False)
    def _prevent_done_deletion(self):
        for record in self:
            if record.state == 'done':
                raise ValidationError(_("You cannot delete completed records."))

    # 6. Safe private internal routine (not exposed to RPC)
    @api.private
    def _recalculate_internal_margins(self):
        # Specific flushing before running custom SQL composition
        self.flush_model(['cost_total'])
        
        query = SQL(
            "SELECT SUM(cost_total) FROM ctieg_task_optimizer WHERE company_id = %s",
            self.env.company.id
        )
        # Safe SQL execution
        results = self.env.execute_query(query)
        return results[0][0] if results else 0.0
```
