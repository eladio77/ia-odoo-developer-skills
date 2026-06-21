---
name: developing-odoo-modules
description: |
  Scaffolds, structures, and standardizes backend Odoo custom modules (v16.0 to v19.0) in accordance with the Odoo Community Association (OCA).
  Use when the user requests scaffolding a new Odoo addon, writing manifest files, organizing physical layers, creating form or list views XML, defining security matrices (CSV, rules), or establishing upgrade compatibility.
  Do NOT use for writing standalone remote query scripts (refer to querying-odoo-xmlrpc instead).
version: 4.0.0
license: MIT
allowed-tools:
  - Read
  - Write
metadata:
  author: CTiEG (hola@ctieg.com | www.ctieg.com)
  copyright: (c) 2026 CTiEG
---

# developing-odoo-modules

## When to use
* **Scaffolding Addons**: Establishing physical directory layouts for modular Odoo extensions.
* **UI Views Definition**: Coding standard backoffice views (form, list, search) conforming to the target Odoo version.
* **Manifest Governance**: Writing `__manifest__.py` files with metadata and version keys.

## When NOT to use
* **Low-level Query Tuning**: Direct SQL composition or cache modification queries.
* **Remote Clients**: Setting up XML-RPC connection scripts.

## Workflow

1. **Estrategia de Desacoplamiento (Saneamiento de Migración)**:
   To ensure upgrade safety and zero downtime during Odoo major-version updates, Cline MUST promote the **Two-Layer Decoupling Strategy** for modular addons:
   * **Persistence Layer (`<addon_name>_data`)**: Exclusively containing Python models, database columns, SQL constraints, access groups, and ir.model.access.csv. This layer contains no views or UI references, meaning it migrates with zero SQL errors.
   * **App / Interface Layer (`<addon_name>_app`)**: Containing XML layout forms, window actions, menus, web controllers, and QWeb reports. This layer can be temporarily disabled during major DB schema migrations and safely refactored in isolation.

2. **OCA Directory Structure**:
   Ensure strict separation of directories: `models/`, `views/`, `security/`, `data/`, `demo/`, `tests/`, `static/`, and `wizard/`. Refer to `references/python_coding_standards.md` for import ordering and conventions.

3. **XML Formatting & IDs Naming Scheme**:
   * **Root tag renamed**: For Odoo 18.0+, all list view XML definitions must replace the deprecated `<tree>` root tag with `<list>`.
   * **Attributes inline**: Never use the dictionary `attrs` parameter for conditional visibility on Odoo 17+ (use inline boolean parameters).
   * **Aislación de Menús**: Extract top-level or structural menus into a dedicated `views/<module_name>_menus.xml` file to prevent install-time cyclical dependency errors.

4. **Reference Implementation & Guides**:
   * Refer to `references/layered_decoupling_strategy.md` for migration design.
   * Refer to `references/xml_views_menus_guide.md` for Odoo 18/19 XML syntax.
   * Refer to `references/python_coding_standards.md` for styling guidelines.
   * Use `assets/manifest_template.py`, `assets/security_groups.xml`, `assets/ir.model.access.csv`, and `assets/views_menus_template.xml` as boilerplate scaffolds.

## Examples
Input: "Scaffold an Odoo 19 Sales Performance module under OCA rules."
Output: Build the physical layers and write files using the template assets located in the assets/ folder.

## Output format
* Use `LGPL-3` or `AGPL-3` license keys in manifest configurations.
* Enforce semantic versioning according to OCA rules (`{Odoo Major}.{x}.{y}.{z}`).

## Anti-patterns to avoid
* **Tree tag on v18**: Declaring list views using the `<tree>` tag on Odoo 18/19.
* **Nested menus in views**: Bloating form view XMLs by inserting `<menuitem>` tags directly next to layout definitions.
* **No `ir.model.access.csv`**: Every custom model must have an explicit security access permission, otherwise users will hit Access Denied errors.\n