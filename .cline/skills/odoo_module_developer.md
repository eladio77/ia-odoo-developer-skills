# Skill: OCA Odoo Module Architecture, Scaffolding, & Standards

This Skill equips the Cline agent with directory structure rules, Python stylistic conventions, view/menu declarations, manifest configuration, and migration-safe decoupling protocols following Odoo and **Odoo Community Association (OCA)** best practices.

---

## ⚡ Architectural Strategy: Database Contract vs UI Separation
To minimize critical failures and simplify database updates during major version upgrades (e.g., v17 → v18, or v18 → v19), Odoo best practice recommends **splitting complex features into two distinct addon modules** [638, 647, 651]:

1. **Persistent Data Module (`ctieg_feature_data`)**:
   * **Scope:** Defines Odoo database models, new fields, model inheritances, SQL constraints, Python validation rules, backend business logic, security permissions (`ir.model.access.csv`), and record rules [638, 647, 651].
   * **Exclusion:** Does NOT contain window actions, menus, XML form/list views, QWeb reports, dashboards, or web controllers [638, 647, 651].
   * **Migration Benefit:** This module remains extremely stable during migrations because database schema upgrades (`OpenUpgrade`) almost never break due to front-end changes [638, 647, 651].

2. **Presentation UI Module (`ctieg_feature_app`)**:
   * **Scope:** Declares the navigation hierarchy, window actions, view structures (form, kanban, list, search, pivot, graph), QWeb printed reports, e-commerce templates, and web controllers [638, 647, 651]. Depends directly on `ctieg_feature_data` [638, 647, 651].
   * **Migration Benefit:** Since XML views and XPath expressions frequently break when Odoo changes parent form structures, this layer can be cleanly uninstalled or disabled before a major database migration [649, 651]. Once the database engine successfully upgrades, the UI module is adapted, tested, and reinstalled independently without risking database data loss [649, 651].

---

## 📁 Strict Directory Structure
An OCA-compliant Odoo module must follow a clean physical separation of responsibilities [6, 211]:
```text
ctieg_addon/
├── __init__.py                  # Root package initializer
├── __manifest__.py              # Addon metadata, dependencies, and file load order
├── data/                        # Static, non-modifiable records (noupdate="1")
├── demo/                        # Sample data used strictly for tests and CI/CD
├── models/                      # Python database model classes (one model per file)
│   ├── __init__.py
│   └── my_model.py
├── security/                    # Security group definitions and access rights CSV
│   ├── ir.model.access.csv
│   └── my_model_security.xml
├── views/                       # Client web views and templates (no menus)
│   └── my_model_views.xml
├── controllers/                 # HTTP/JSON-RPC web controllers
├── static/                      # Frontend assets (src/js, src/scss, src/xml, img)
├── tests/                       # Unit tests (tests/test_my_model.py)
└── wizard/                      # Transient models and their respective views
```

---

## 🐍 Python Coding Conventions & Standards
* **Imports Order:** Group imports alphabetically in three distinct blocks separated by single empty lines [220]:
  1. Python standard library imports [220].
  2. Odoo core framework imports [220].
  3. Other Odoo addons imports (rare, declared only if mandatory) [220].
* **Context Propagation:** When calling methods with an altered context, always use the `with_context()` method rather than modifying the environment dictionary directly [224].
  * *Warning:* Avoid inserting values that could conflict with third-party creations (such as `default_my_field` during broad transactional creations) [224]. Always prefix custom context keys with your module name to isolate side effects [225].
* **Singular Naming Scheme:** Model names and module directories must be singular [234, 871] (e.g., `ctieg_order` and `ctieg.order`, NOT `ctieg_orders` or `ctieg.orders`).

---

## 🎨 XML Views, Menus, & XPath Standards

1. **XPath Robustness (Inherited Views):**
   * **Avoid positional routing:** Never target views using index paths (e.g., `//form/sheet/notebook/page[2]/group/div`) as these change continuously across Odoo versions, breaking your module [404, 649].
   * **Anchor on stable attributes:** Anchor XPath selections strictly on unique attributes like `name`, `id`, or specific field tags [404, 649].
     * *Recommended:* `//field[@name='partner_id']` or `//group[@name='metrics_group']` [404].

2. **Clean Menu Placement:**
   * Do not embed top-level menus or navigation trees inside a specific model's layout view [214].
   * Separate menu structure definitions into a dedicated file named `views/<module_name>_menus.xml` to avoid cyclic XML loading dependencies [214].

3. **Structural Tree Tag Obsolescence:**
   * **Odoo 17:** Remove the `attrs` attribute entirely [13]. Set conditions using inline boolean expressions [13]:
     `invisible="state != 'draft'" readonly="state == 'done'" required="estimated_hours > 5"` [418, 978].
   * **Odoo 18 / 19:** The `<tree>` tag is completely deprecated [15, 637]. You must rename the root tag of all list and table views to `<list>` [15, 637]:
     ```xml
     <list string="Tasks list">
         <field name="name"/>
     </list>
     ```

---

## ⚙️ Manifest & Community Extras Configuration
* **Version Format:** Use the official OCA semantic version scheme [6, 975]:
  `{Odoo_Major}.{x}.{y}.{z}` (e.g., `19.0.1.0.0` for a module targeting Odoo 19) [6, 975].
* **Conditional Dependencies (`depends_if_installed`)**:
  Using the `base_manifest_extension` OCA addon, you can declare optional dependencies inside your manifest [22, 465]. This allows your module to integrate with optional third-party modules dynamically *only if* they are already installed, preventing hard installation blocks [466]:
  ```python
  "depends_if_installed": {
      "crm": ["views/crm_extensions.xml"]
  }
  ```

---

## 📦 Complete Scaffolding: Sales Performance App Template (Odoo 19)

### 1. Manifest: `__manifest__.py`
```python
# -*- coding: utf-8 -*-
{
    "name": "CTiEG Sales Performance App",
    "summary": "Standardized Sales Performance optimizer for agenic development",
    "version": "19.0.1.0.0",
    "category": "Sales",
    "author": "CTiEG",
    "website": "https://www.ctieg.com",
    "license": "LGPL-3",
    "depends": [
        "sale_management",
        "mail"
    ],
    "data": [
        "security/sales_performance_groups.xml",
        "security/ir.model.access.csv",
        "views/sales_performance_optimizer_views.xml",
        "views/sales_performance_menus.xml"
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
```

### 2. Groups XML: `security/sales_performance_groups.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <record id="module_category_sales_performance" model="ir.module.category">
            <field name="name">Sales Performance</field>
            <field name="sequence">25</field>
        </record>

        <record id="group_sales_performance_user" model="res.groups">
            <field name="name">Performance Analyst</field>
            <field name="category_id" ref="module_category_sales_performance"/>
            <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
        </record>
    </data>
</odoo>
```

### 3. Matriz CSV: `security/ir.model.access.csv`
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_sales_performance_user,sales.performance.user,model_ctieg_task_optimizer,group_sales_performance_user,1,1,1,0
```

### 4. Vistas XML: `views/sales_performance_optimizer_views.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- List view (Mandatory tag <list> in Odoo 18/19) -->
    <record id="ctieg_task_optimizer_view_list" model="ir.ui.view">
        <field name="name">ctieg.task.optimizer.view.list</field>
        <field name="model">ctieg.task.optimizer</field>
        <field name="arch" type="xml">
            <list string="Optimized Tasks" decoration-info="state == 'draft'" decoration-success="state == 'done'">
                <field name="sequence" widget="handle"/>
                <field name="name"/>
                <field name="partner_id"/>
                <field name="estimated_hours" sum="Total Hours"/>
                <field name="cost_total" sum="Total Cost"/>
                <field name="state" widget="badge"/>
            </list>
        </field>
    </record>

    <!-- Form view displaying inline dynamic attributes instead of obsolete attrs dictionary -->
    <record id="ctieg_task_optimizer_view_form" model="ir.ui.view">
        <field name="name">ctieg.task.optimizer.view.form</field>
        <field name="model">ctieg.task.optimizer</field>
        <field name="arch" type="xml">
            <form string="Optimizer Form">
                <header>
                    <button name="action_confirm" string="Confirm" type="object" class="oe_highlight" invisible="state != 'draft'"/>
                    <field name="state" widget="statusbar" statusbar_visible="draft,progress,done"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1>
                            <field name="name" placeholder="E.g., Client Optimization Strategy"/>
                        </h1>
                    </div>
                    <group>
                        <group name="customer_data">
                            <field name="partner_id" readonly="state == 'done'"/>
                            <field name="company_id" readonly="state == 'done'"/>
                        </group>
                        <group name="metrics_data">
                            <field name="estimated_hours" readonly="state == 'done'"/>
                            <field name="discount_rate" readonly="state == 'done'" required="estimated_hours > 10"/>
                            <field name="cost_total"/>
                        </group>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <record id="ctieg_task_optimizer_action" model="ir.actions.act_window">
        <field name="name">Optimizer Activity</field>
        <field name="res_model">ctieg.task.optimizer</field>
        <field name="view_mode">list,form</field>
    </record>
</odoo>
```

### 5. Menús XML: `views/sales_performance_menus.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Isolate top-level menus to prevent cyclic dependencies during XML installation -->
    <menuitem id="menu_sales_performance_root" 
              name="CTiEG Performance" 
              parent="sale.menu_sale_config" 
              sequence="80"/>

    <menuitem id="menu_ctieg_task_optimizer" 
              name="Optimization Actions" 
              parent="menu_sales_performance_root" 
              action="ctieg_task_optimizer_action" 
              sequence="10"/>
</odoo>
```
