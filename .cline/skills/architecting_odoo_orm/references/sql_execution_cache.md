# Odoo 19 SQL Execution & Cache Management

Odoo delays database persistence for performance reasons, meaning some computed fields or updates remain in the memory cache before being written to PostgreSQL.

## execute_query vs cr.execute
Odoo 19 introduces `self.env.execute_query()` as a safe, cache-aware SQL execution method.

```python
# Safe, composable query with automatic dependency metadata injection
from odoo.tools import SQL
query = SQL(
    "SELECT id, name FROM res_partner WHERE country_id = %s", 
    country_id
)
records = self.env.execute_query(query)
```

## Transaction Cache Governance

When executing custom SQL statements, you bypass the ORM layer entirely. You MUST manually handle Odoo's caches:

1. **Flush cache**: Force write Odoo memory modifications to PostgreSQL before executing the SQL statement:
   `self.flush_model(fnames)` or `self.flush_recordset(fnames)`
2. **Invalidate cache**: Clear outdated memory caches after execution:
   `self.invalidate_model(fnames)` or `self.invalidate_recordset(fnames)`
3. **Notify changes**: Inform Odoo's dependency engine that fields have been modified to trigger dependent calculations:
   `self.modified(fnames)`\n