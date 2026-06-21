---
name: architecting-odoo-orm
description: |
  Optimizes database queries, transaction boundaries, and computed fields in Odoo 19.0.
  Use when the user requests database query performance tuning, fixing N+1 database bottlenecks, writing computed fields with depends context, executing raw SQL securely, or invalidating the ORM cache.
  Do NOT use for creating remote connections over XML-RPC or JSON-2 (refer to querying-odoo-xmlrpc instead).
version: 4.0.0
license: MIT
allowed-tools:
  - Read
  - Write
metadata:
  author: CTiEG (hola@ctieg.com | www.ctieg.com)
  copyright: (c) 2026 CTiEG
---

# architecting-odoo-orm

## When to use
* **Database Performance Tuning**: Preventing massive relational loop queries by leveraging recordset bulk operations.
* **Secure SQL Composition**: Writing parameterized raw database statements using Odoo 19's SQL wrappers.
* **Transactional Caching**: Managing cache coherency when writing low-level database scripts.

## When NOT to use
* **External APIs**: Writing standalone HTTP client scripts.
* **Andamiaje de Módulos**: Setting up manifest files, directory rules, or views XML.

## Workflow

1. **Evitación de Consultas en Ciclos (Problema N+1)**:
   * **Enforce Prefetching**: Never search or browse individual record IDs inside Python `for` loops. Iterate over bulk recordsets so that Odoo's prefetching cache loads fields in a single PostgreSQL query trip.
   * **Avoid Loops on write()**: Write values in batch (`records.write({'state': 'confirmed'})`) instead of loop iterations.
   * **Database-level Aggregation**: Do NOT sum or average fields in Python loops. Always use `_read_group()` to push calculations directly to PostgreSQL.

2. **Gobernanza Transaccional y de Caché**:
   * **Strictly Prohibit Manual Commits**: Cline is forbidden from calling `cr.commit()` or `cr.rollback()` in custom backend logic, as this breaks test rollbacks and triggers severe data inconsistencies.
   * **Use Savepoints**: To isolate potential errors safely within loop structures, use transaction savepoints: `with self.env.cr.savepoint():`

3. **Secure SQL Composition (Odoo 19 Standards)**:
   * **Prohibit Direct `cr.execute()` Concatenations**: Prevent SQL injection by composing queries exclusively with the `odoo.tools.SQL` wrapper and executing them using `self.env.execute_query(sql)`.
   * **Manage Cache Flush and Invalidation**: Before running direct SQL, flush Odoo's model cache (`self.flush_model()`). After execution, invalidate the records cache (`self.invalidate_model()`) and alert Odoo of changed fields using `self.modified()`.

4. **Reference Implementation & Guides**:
   * Refer to `references/orm_performance.md` for prefetching mechanisms.
   * Refer to `references/sql_execution_cache.md` for Odoo 19 cache-aware query patterns.
   * Refer to `references/odoo19_deprecations.md` for deprecated API calls.
   * Use `assets/task_optimizer_model.py` as a complete, OCA-compliant model baseline.

## Examples
Input: "Write an aggregate query to get the sum of hours grouped by partner."
Output: Refer to `_read_group()` usage inside `references/orm_performance.md`.

## Output format
* All backend code must use proper Odoo 19 imports.
* Computed methods must be private, starting with a single underscore.

## Anti-patterns to avoid
* **`record._cr` usage**: Use `record.env.cr` instead.
* **`read_group` calls**: Deprecated in Odoo 18; use `_read_group()` instead.
* **No `ensure_one()`**: Forgetting to add `self.ensure_one()` at the start of instance methods.\n