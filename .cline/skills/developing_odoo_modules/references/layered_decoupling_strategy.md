# Layered Decoupling Strategy for Odoo Custom Addons

Major version upgrades are high-risk operations in ERP life cycles, usually causing data loss or severe downtime because layout views break under updated database schemas.

## The Decoupling Pattern

To isolate physical data from volatile visual layouts, we split a feature into two distinct addons:

### 1. Persistence Layer (`my_module_data`)
* **Contains**: Models, fields, PostgreSQL indexes, security groups, model access CSV, data files (`noupdate="1"`).
* **Restrictions**: Absolutely NO XML views, menus, window actions, or QWeb reports.
* **Migration Advantage**: It can be migrated first and safely. It carries zero UI dependencies, preventing OpenUpgrade schema migration crashes.

### 2. Application Layer (`my_module_app`)
* **Contains**: Views, actions, menus, reports, SCSS assets, web controllers.
* **Restrictions**: Declares no new database fields (only inherits view behaviors).
* **Migration Advantage**: Can be safely uninstalled or disabled before schema updates, preventing UI breakage from locking the main database migration process.\n