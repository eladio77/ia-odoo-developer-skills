# Skill: Odoo ORM Architecture, Decorators, and Performance Optimization

This Skill empowers the Cline agent with advanced database engineering guidelines, clean transactional patterns, and critical framework changes from version 16.0 through 19.0 for Odoo backend development.

## Clean and Concise Code

0. **Clean and Concise Code**:
   - Do not generate unnecessary comments in the generated code. Code should be self-explanatory.
   - Prioritize clarity through descriptive variable and function names, not through comments.
   - Be concise: generate only the essential code needed to solve the task, without redundant explanations.
   - Comments are only allowed to document complex, non-obvious business logic that cannot be expressed with descriptive names.

## Performance Principles and N+1 Problem Avoidance

The Odoo ORM dynamically translates Python object operations into PostgreSQL relational queries. Careless design can generate network and database bottlenecks due to the **N+1** antipattern (executing one query per iterated record).

1. **Recordsets and Prefetching**:
   - Odoo uses the *prefetching* mechanism. When iterating over a recordset (e.g., obtained via `search`), the engine caches the identifiers (`ids`) of all records in the set.
   - When accessing a field of a record in a loop for the first time, the ORM performs **a single SQL batch query** to retrieve the value of that field for *all* records in the prefetch set at once.
   - **Antipattern**: Searching or instantiating records individually inside a loop using `browse(id)` or repetitive unit searches. This breaks preloading and degrades performance to $\mathcal{O}(N)$ independent queries instead of a unified $\mathcal{O}(1)$ transaction.

2. **Numeric Aggregations via Database (`_read_group`)**:
   - Never calculate sums, averages, or complex metrics by iterating recordsets in Python.
   - Mandatorily use the `_read_group()` function (or ORM aggregate operations) to offload mathematical computation directly to PostgreSQL via `GROUP BY` clauses and native aggregate instructions (`SUM`, `AVG`, `MAX`), reducing web server RAM consumption.

3. **Bulk Operations (Bulk Writes)**:
   - Avoid at all costs writing values field by field inside iterative loops.
   - **Antipattern**:
     ```python
     for order in orders:
         order.write({'state': 'confirmed'})
     ```
   - **Optimized**:
     ```python
     orders.write({'state': 'confirmed'})
     ```

---

## Transactional Guidelines and Error Handling

1. **Transactional Governance**:
   - **Strict Rule**: Do not manually call `cr.commit()` or `cr.rollback()` in business or test code, unless you have explicitly initialized your own database cursor (`self.env.registry.cursor()`).
   - The framework automatically manages transaction boundaries (opening a transaction at the start of an RPC call, committing at the end, and performing a full rollback on any uncaught error).
   - Calling a partial commit causes critical data inconsistencies, stuck documents, and corrupts automated test systems by preventing QA environments from cleaning the database after tests.

2. **Explicit Exception Handling and Savepoints**:
   - Catch only specific exceptions (`UserError`, `ValidationError`, `AccessError`) defined in `odoo.exceptions`. Avoid generic `except Exception:` blocks.
   - If you need to implement a retry process or isolate errors within a loop without aborting the main Odoo transaction, use **transactional savepoints** via `with self.env.cr.savepoint():`. This ensures PostgreSQL can locally revert failed changes without invalidating the entire transaction.
   - *Performance note*: PostgreSQL degrades speed after exceeding 64 active savepoints within the same transaction. Limit the batch size processed.

---

## Evolution of Decorators in Odoo API

Use Odoo ORM-provided method decorators precisely to dictate model behavior:

*   `@api.depends(*fields)`: The computed fields engine. Recalculates the field value only when any of the declared fields in the list changes value. Avoid overloads by preventing unnecessary dependencies or redundant dotted paths.
*   `@api.constrains(*fields)`: Backend business logic validator. Executes when saving or updating records in the database. Must raise a `ValidationError` if rules are violated. Only supports fields from the model itself (no complex dotted paths).
*   `@api.onchange(*fields)`: Visual interactivity in the web client. Executes on a temporary simulated record in the browser upon form changes in the front-end. Does not allow direct database operations (`create`, `write`, `unlink`) since the record may not physically exist yet.
*   `@api.model_create_multi`: **Mandatory for `create` overrides**. Decorates the creator method to accept a list of value dictionaries. Allows the ORM to optimize persisting multiple new records in a single PostgreSQL insert, massively accelerating imports and detail line creation.
*   `@api.ondelete(*, at_uninstall=False)**: Registers a validation method to execute when deleting (`unlink`) records. Allows raising user exceptions (such as preventing deletion of an invoiced order). Keep `at_uninstall=False` to avoid errors during clean module uninstallation on CI/CD servers.
*   `@api.depends_context(*keys)`: Specifies external contextual dependencies (such as `company`, `uid`, or `lang`) for non-persisted computed fields in the database.
*   `@api.private`: Completely hides the function from RPC mapping. Ensures no external system or client can call the function remotely for security reasons.

---

## Critical Major Version Changes (v16.0 to v19.0)

When auditing, writing, or migrating Odoo code, strictly follow these version rules:

### 1. Complete removal of `attrs` in views (v17.0+)
- **v16.0 or lower**: The XML dictionary attribute `attrs="{'invisible': [('state', '=', 'draft')]}"` was used.
- **v17.0 onward**: Completely prohibited. Use inline dynamic boolean attributes instead:
  ```xml
  <field name="partner_id" invisible="state == 'draft'" readonly="state != 'draft'" required="state == 'confirmed'"/>
  ```

### 2. Structural change from `<tree>` to `<list>` (v18.0+)
- **v17.0 or lower**: List views were declared under the `<tree>` root tag.
- **v18.0 and v19.0**: The `<tree>` tag is deprecated and removed in v18. The tag must be mandatorily renamed to `<list>` in any XML list definition:
  ```xml
  <list string="Records">
      <field name="name"/>
  </list>
  ```

### 3. Deprecation and Extinction of `name_get()` (v17.0 and v18.0+)
- **v16.0 or lower**: `name_get(self)` was overridden to return a list of tuples `[(id, display_name), ...]`.
- **v17.0**: The computed method `_compute_display_name(self)` is introduced to manage record name display.
- **v18.0 and v19.0**: The classic `name_get()` method is extinct. Any customization of a relational record label must be done by overriding Odoo's native computed method:
  ```python
  def _compute_display_name(self):
      for record in self:
          record.display_name = f"[{record.reference}] {record.name}"
  ```

### 4. Multi-company Security Governance
- Set `_check_company_auto = True` on the model and decorate relational fields (`Many2one`, `Many2many`) with `check_company=True` to force the ORM to automatically validate that records from different companies are not linked in cross-company transactions.

---

## Reference Data Model (v18.0 / v19.0)

This template brings together all the professional standards previously outlined:

```python
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

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
    ], string="Status", default="draft", required=True)

    company_id = fields.Many2one(
        'res.company', string="Company",
        default=lambda self: self.env.company, required=True
    )

    partner_id = fields.Many2one(
        'res.partner', string="Customer",
        check_company=True, index="btree"
    )

    estimated_hours = fields.Float(string="Estimated Hours")
    discount_rate = fields.Float(string="Discount Rate", default=0.0)

    cost_total = fields.Monetary(
        compute="_compute_cost_total",
        currency_field="currency_id",
        store=True
    )

    currency_id = fields.Many2one(
        'res.currency', related="company_id.currency_id", store=True
    )

    @api.depends('name', 'state')
    def _compute_display_name(self):
        for record in self:
            state_label = dict(self._fields['state'].selection(self)).get(record.state, '')
            record.display_name = f"[{state_label.upper()}] {record.name}"

    @api.depends('estimated_hours', 'discount_rate')
    def _compute_cost_total(self):
        for record in self:
            base_rate = 50.0
            net_rate = base_rate * (1.0 - (record.discount_rate / 100.0))
            record.cost_total = record.estimated_hours * net_rate

    @api.constrains('estimated_hours', 'discount_rate')
    def _check_task_values(self):
        for record in self:
            if record.estimated_hours <= 0:
                raise ValidationError(_("Estimated hours must be a strictly positive value."))
            if not (0.0 <= record.discount_rate <= 100.0):
                raise ValidationError(_("Discount rate must be between 0% and 100%."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = _("Untitled task")
        return super().create(vals_list)

    @api.ondelete(at_uninstall=False)
    def _prevent_done_deletion(self):
        for record in self:
            if record.state == 'done':
                raise ValidationError(_("Cannot delete records in 'Completed' status."))