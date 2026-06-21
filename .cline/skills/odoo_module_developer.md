---
name: developing-odoo-modules
description: |
  Scaffolds, structures, and standardizes custom Odoo modules/addons according to official guidelines and Odoo Community Association (OCA) best practices from v16.0 to v19.0. Use this skill when the user asks to create a new module, define view layouts, manage access security files (CSV/rules), or migrate menus and actions.
  Do NOT use for optimizing backend SQL queries, debugging low-level ORM calculations, or writing remote integration scripts.
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

# Developing Odoo Modules

## When to use
* **Addon Scaffolding**: Creating the physical directory structure, initial manifest, and initialization python files for a new Odoo module.
* **UI Design (Form, List, Kanban)**: Designing user interface layouts, declaring window actions, and setting up nested navigation menus.
* **Security & Access Rights**: Establishing CSV model access matrices (`ir.model.access.csv`), security XML categories, user groups, and row-level record rules.
* **Addon Migration Prep**: Upgrading XML view tags, moving away from legacy attributes (like `attrs`), and refactoring layouts for Odoo 18/19 compatibility.

## When NOT to use
* **Query Performance Tuning**: Optimizing heavy loops, database queries, prefetching parameters, or SQL views.
* **External Integrations**: Writing client scripts utilizing XML-RPC, JSON-RPC, or External JSON-2 API endpoints.
* **Frontend Web Library Development**: Developing custom client actions, JS extensions, or custom OWL components.

## Workflow
1. **Apply Layered Decoupling Strategy (Migration Insurance)**:
   * For medium-to-large business critical projects, separate your customizations into two distinct module layers:
     1. **Data Layer (`custom_module_data`)**: Exclusively defines Python models, fields, sql constraints, security files (CSV and XML groups/rules), and master parametrizations. No views, menus, actions, or reports.
     2. **Application Layer (`custom_module_app`)**: Defines views, menus, actions, window actions, QWeb report actions, web controllers, and assets. Depends directly on the data layer.
   * **Why**: Views and menus are highly fragile and prone to breaking during major version updates (e.g., 17 → 18 → 19). Splitting them lets you disable/uninstall the application layer safely before upgrading the database. This protects your persistent data and tables from schema validation crashes. You can then fix and reinstall the visual layer methodically post-upgrade.
2. **Scaffold with Strict Directory Structure**:
   Ensure files are structured inside standard folders to isolate concerns:
   * `data/`: Static configurations, sequences, and master records (use `noupdate="1"`).
   * `demo/`: Fake data for automated unit tests / continuous integration.
   * `models/`: Python files containing ORM models (one main class per file).
   * `security/`: Access controls CSV and XML security groups/record rules.
   * `views/`: XML files containing list, form, kanban, or search views.
   * `wizard/`: Transient models (`models.TransientModel`) and their temporary views.
3. **Align Manifest with OCA Rules**:
   * Version number must follow the semantic OCA format: `{Odoo Major}.{x}.{y}.{z}` (e.g., `18.0.1.0.0` for the first stable release on Odoo 18).
   * Specify clear metadata: `license` (prefer `LGPL-3` or `AGPL-3`), `website`, `author` (CTiEG), and `category`.
   * To prevent hard-dependencies on optional modules, leverage **`depends_if_installed`** to dynamically load compatibility XML files only if those modules exist in the active database.
4. **Implement Robust XML Formatting & Naming Schemes**:
   * Order field parameters predictably. Place the `id` attribute before the `model` in records.
   * **Strict XML ID Naming Conventions**:
     * **Menus**: `<model_name>_menu` (or `<model_name>_menu_do_stuff` for submenus).
     * **Views**: `<model_name>_view_<type>` (e.g., `project_task_view_form`, `project_task_view_list`).
     * **Actions**: `<model_name>_action`.
     * **Groups**: `<module_name>_group_<name>` (e.g., `sales_performance_group_user`).
     * **Record Rules**: `<model_name>_rule_<concerned_group>` (e.g., `project_task_rule_company`).
   * **XPath Inheritance Rule**: Always anchor on stable, unique attributes (e.g., `name` or `id`) when patching views (e.g., `//field[@name="partner_id"]`). **Never** use positional paths (e.g., `//form/sheet/page[2]/div`) which break silently when upstream parent layouts change. Suffix inherited view names with `.inherit.{details}`.
5. **Enforce Odoo 18/19 Views Compliance**:
   * **No `<tree>` tags**: Tree views in v18+ are fully deprecated. All tabular backoffice view structures must use the **`<list>`** tag.
   * **No `attrs` attribute**: Conditional visibility/editing dictionary strings (e.g., `attrs="{'invisible': [('state', '=', 'draft')]}"`) are fully abolished in v17+. Use inline direct attributes: `invisible="state == 'draft'"` or `readonly="state != 'draft'"` or `required="state == 'confirmed'"`.
6. **Isolate Menus**:
   * Extract all menu navigation mappings to a dedicated `views/<module_name>_menus.xml` file instead of dispersing them across individual view files. This prevents dependency order errors and missing reference crashes.

## Examples

### Example 1: OCA-Compliant Manifest (`__manifest__.py`)
```python
# -*- coding: utf-8 -*-
{
    "name": "Sales Performance Optimizer",
    "summary": "Advanced sales tracking and performance optimization analysis",
    "version": "18.0.1.0.0",  # Strict OCA Major.x.y.z format
    "category": "Sales",
    "author": "CTiEG",
    "license": "LGPL-3",
    "website": "https://www.ctieg.com",
    "depends": [
        "sale_management",
        "mail"
    ],
    # Dynamic conditional loading to prevent hard dependencies
    "depends_if_installed": {
        "board": ["views/sales_performance_dashboard.xml"]
    },
    "data": [
        "security/sales_performance_groups.xml",
        "security/ir.model.access.csv",
        "views/sales_performance_optimizer_views.xml",
        "views/sales_performance_menus.xml"  # Menus loaded separately
    ],
    "demo": [
        "demo/sales_performance_demo.xml"
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
```

### Example 2: Access Rules Matrix (`security/ir.model.access.csv`)
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_sales_performance_user,sales.performance.user,model_project_task_optimizer,group_sales_performance_user,1,1,1,0
access_sales_performance_manager,sales.performance.manager,model_project_task_optimizer,group_sales_performance_manager,1,1,1,1
```

### Example 3: Decoupled View Layout File (`views/sales_performance_optimizer_views.xml`)
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Tabular List View (mandatory <list> tag replacing deprecated <tree> in Odoo 18+) -->
    <record id="project_task_optimizer_view_list" model="ir.ui.view">
        <field name="name">project.task.optimizer.view.list</field>
        <field name="model">project.task.optimizer</field>
        <field name="arch" type="xml">
            <list string="Optimization Tasks" decoration-info="state == 'draft'" decoration-success="state == 'done'">
                <field name="sequence" widget="handle"/>
                <field name="name"/>
                <field name="partner_id"/>
                <field name="estimated_hours" sum="Total Hours"/>
                <field name="cost_total" sum="Total Cost"/>
                <field name="state" widget="badge"/>
            </list>
        </field>
    </record>

    <!-- Detailed Form View featuring direct inline attributes (abolished attrs) -->
    <record id="project_task_optimizer_view_form" model="ir.ui.view">
        <field name="name">project.task.optimizer.view.form</field>
        <field name="model">project.task.optimizer</field>
        <field name="arch" type="xml">
            <form string="Optimization Task">
                <header>
                    <button name="action_confirm" string="Confirm" type="object" class="oe_highlight" invisible="state != 'draft'"/>
                    <field name="state" widget="statusbar" statusbar_visible="draft,progress,done"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1>
                            <field name="name" placeholder="E.g., Remodeling Blueprint Task..."/>
                        </h1>
                    </div>
                    <group name="main_group">
                        <group name="left_details">
                            <field name="partner_id" readonly="state == 'done'"/>
                            <field name="company_id" readonly="state == 'done'"/>
                        </group>
                        <group name="right_metrics">
                            <field name="estimated_hours" readonly="state == 'done'"/>
                            <!-- Direct inline conditional requirements -->
                            <field name="discount_rate" readonly="state == 'done'" required="estimated_hours > 10"/>
                            <field name="cost_total"/>
                        </group>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <!-- Windows Action Mapping -->
    <record id="project_task_optimizer_action" model="ir.actions.act_window">
        <field name="name">Performance Analysis</field>
        <field name="res_model">project.task.optimizer</field>
        <field name="view_mode">list,form</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Create your first sales performance optimization record.
            </p>
        </field>
    </record>
</odoo>
```

## Output format
Standard addons generated by this skill must be packaged using:
* Clean, modular python code structured inside `models/` with proper header encodings `# -*- coding: utf-8 -*-` and PEP8 import blocks.
* Clean XML views formatted using a 4-space indentation system, with direct inline attributes instead of obsolete `attrs`.
* Isolated view configurations (`*_views.xml`) and menu definitions (`*_menus.xml`).
* Complete CSV security matrix lists detailing basic user and administrator access permissions.

## Anti-patterns to avoid
* **DO NOT** declare menu items (`<menuitem>`) inside files dedicated to model form views or list views. Keep menus isolated to prevent loading reference crashes.
* **DO NOT** use positional XPath paths (`//form/sheet/page[2]/div`) which immediately break upon minor upstream updates. Use attribute anchoring instead.
* **DO NOT** use the obsolete `<tree>` tag for list views in Odoo 18 or 19.
* **DO NOT** write business logic inside views. Business rules must reside exclusively inside model methods.
* **DO NOT** mix models and views inside a single addon in large scale projects where structural migration separation is required.
