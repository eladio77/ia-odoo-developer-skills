# Odoo 19 Backend Deprecations & Replacements

Ensure Cline never utilizes deprecated methods or APIs. Use this list during code refactoring:

| Deprecated Call | Odoo 19 Replacement | Notes |
| :--- | :--- | :--- |
| `record._cr` | `record.env.cr` | Direct cursor access deprecated. |
| `record._context` | `record.env.context` | Use the environment context directly. |
| `record._uid` | `record.env.uid` | Extract UID from Environment. |
| `name_get()` | `_compute_display_name()` | Extinct in Odoo 18; must override display_name. |
| `read_group()` | `_read_group()` | Deprecated in Odoo 18.0; use native _read_group. |
| `odoo.osv` | *None* | Legacy osv namespace is fully deprecated. |
| `attrs="..."` | Atributes inline | XML `attrs` attribute deleted. Use inline `invisible`, `readonly`. |
| `<tree>` | `<list>` | Listview root tag renamed in v18. |\n