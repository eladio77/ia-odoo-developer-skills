# Skill: Backend Module Structuring and OCA Standards for Odoo

This Skill empowers the Cline agent with physical layer design protocols, strict naming conventions from the Odoo Community Association (OCA), professional scaffolding, and decoupling strategies to minimize friction during major Odoo migrations (v16.0 to v19.0).

## Clean and Concise Code

0. **Clean and Concise Code**:
   - Do not generate unnecessary comments in the generated code. Code should be self-explanatory.
   - Prioritize clarity through descriptive variable and function names, not through comments.
   - Be concise: generate only the essential code needed to solve the task, without redundant explanations.
   - Comments are only allowed to document complex, non-obvious business logic that cannot be expressed with descriptive names.

## Architecture Strategy: Data and Application (UI) Decoupling

To mitigate recurring failures and operational complexity during major version migrations (e.g., from v17 to v18, or v18 to v19), it is formally recommended to implement a **two-layer physical separation strategy** for moderate to high complexity developments:

1. **Data and Persistence Layer (`mi_modulo_data`)**:
   - **Content**: Exclusive definition of Python models, field extensions, SQL constraints (`_sql_constraints`), hard backend business logic, physical security files (`ir.model.access.csv` and record rules), and basic parametrization data.
   - **Exclusion**: Must not contain XML UI views (`form`, `list`, `kanban`), menus, window actions, QWeb reports, dashboards, or front-end resources.
   - **Migration Advantage**: This layer almost never experiences errors during database update processes (`OpenUpgrade` or official service), allowing SQL schemas to be migrated and validated cleanly and as a priority.

2. **Interface and User Experience Layer (`mi_modulo_app`)**:
   - **Content**: Declaration of window actions, UI views, general menus, printed reports, HTTP web controllers, and static resources (`JS/SCSS/OWL`). Depends directly on `mi_modulo_data`.
   - **Migration Advantage**: Since it contains XMLs and XPath interfaces prone to breaking due to structural changes in base Odoo, this layer can be safely uninstalled or disabled before database migration without risking persisted data. Once the database engine is migrated, the development team adapts, fixes, and reinstalls the visual layer in an isolated and controlled manner.

---

## Physical Layer Organization and OCA Standards

Each addon must maintain a strict physical directory hierarchy to separate responsibilities. Never scatter general menus or static resources across model files.

### Standard Directory Structure
```text
mi_modulo/
├── __init__.py
├── __manifest__.py
├── data/
├── demo/
├── models/
│   ├── __init__.py
│   ├── mi_modelo_base.py
│   └── mi_modelo_extension.py
├── security/
│   ├── ir.model.access.csv
│   └── mi_modelo_security.xml
├── views/
│   ├── mi_modelo_base_views.xml
│   └── mi_modulo_menus.xml
├── controllers/
├── static/
├── tests/
└── wizard/
```

### Manifest Naming Rules and Versioning
- **License**: Use open-source licenses compatible and authorized by the OCA, prioritizing `LGPL-3` or `AGPL-3`.
- **OCA Semantic Versioning**: The version number must strictly follow the pattern:
  $$\text{Version: } \{\text{Odoo Major}\} \cdot \{\text{x}\} \cdot \{\text{y}\} \cdot \{\text{z}\}$$
  *Example*: `18.0.1.0.0` (Module compiled for Odoo 18.0, first stable release version).
- **depends_if_installed**: Leverage dynamic optional dependencies to inject compatibility with third-party modules only if they coexist in the installed database, avoiding hard cross-dependencies.

---

## XML Guidelines and UI Best Practices (v18.0 and v19.0)

1. **Menu Separation**:
   Do not embed general menus in model business views. Extract the entire navigation organizational structure to a dedicated file `views/<module>_menus.xml`. This prevents XML inheritance issues and unresolved IDs during the sequential installation process.

2. **Safe View Inheritance (Robust XPath)**:
   When extending standard Odoo views, avoid using positional XPath routes that depend on the physical element hierarchy (`//form/sheet/notebook/page[2]/group/div`). These structures are extremely fragile and break with every Odoo update.
   - **Best Practices**: Anchor searches on stable attributes (`name`, `id`, or key control fields).
     *Recommended Example*: `//field[@name="partner_id"]` or `//notebook[@name="main_notebook"]`.

3. **list Version Constraint (v18+)**:
   Immediately replace the `<tree>` structural tag with `<list>` in any list view or editable subform from Odoo v18.0 onward.

---

## Professional Backend Module Scaffolding (v18.0 / v19.0)

Below is the complete structuring of the decoupled sales performance analysis module `sales_performance_optimizer`:

### 1. Manifest File: `__manifest__.py`
```python
{
    "name": "Sales Performance Optimizer (OCA Standard)",
    "summary": "Advanced analytics for sales team goals and performance",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "author": "NotebookLM OCA Developer",
    "license": "LGPL-3",
    "website": "https://odoo-community.org",
    "depends": [
        "sale_management",
        "mail"
    ],
    "depends_if_installed": {
        "board": ["views/sales_performance_dashboard.xml"]
    },
    "data": [
        "security/sales_performance_groups.xml",
        "security/ir.model.access.csv",
        "views/sales_performance_optimizer_views.xml",
        "views/sales_performance_menus.xml"
    ],
    "demo": [
        "demo/sales_performance_demo.xml"
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
```

### 2. Security Groups XML Definition: `security/sales_performance_groups.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <record id="module_category_sales_performance" model="ir.module.category">
            <field name="name">Sales Performance</field>
            <field name="sequence">20</field>
        </record>

        <record id="group_sales_performance_user" model="res.groups">
            <field name="name">Analysis User</field>
            <field name="category_id" ref="module_category_sales_performance"/>
            <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
        </record>

        <record id="group_sales_performance_manager" model="res.groups">
            <field name="name">Analysis Manager</field>
            <field name="category_id" ref="module_category_sales_performance"/>
            <field name="implied_ids" eval="[(4, ref('group_sales_performance_user'))]"/>
            <field name="users" eval="[(4, ref('base.user_root')), (4, ref('base.user_admin'))]"/>
        </record>
    </data>
</odoo>
```

### 3. Access Control CSV Matrix: `security/ir.model.access.csv`
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_sales_performance_user,sales.performance.user,model_project_task_optimizer,group_sales_performance_user,1,1,1,0
access_sales_performance_manager,sales.performance.manager,model_project_task_optimizer,group_sales_performance_manager,1,1,1,1
```

### 4. Business Views XML Definition (v18+ List Format): `views/sales_performance_optimizer_views.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="project_task_optimizer_view_list" model="ir.ui.view">
        <field name="name">project.task.optimizer.view.list</field>
        <field name="model">project.task.optimizer</field>
        <field name="arch" type="xml">
            <list string="Task Optimizer" decoration-info="state == 'draft'" decoration-success="state == 'done'">
                <field name="sequence" widget="handle"/>
                <field name="name"/>
                <field name="partner_id"/>
                <field name="estimated_hours" sum="Total Hours"/>
                <field name="cost_total" sum="Total Cost"/>
                <field name="state" widget="badge"/>
            </list>
        </field>
    </record>

    <record id="project_task_optimizer_view_form" model="ir.ui.view">
        <field name="name">project.task.optimizer.view.form</field>
        <field name="model">project.task.optimizer</field>
        <field name="arch" type="xml">
            <form string="Task Optimizer">
                <header>
                    <button name="action_confirm" string="Confirm" type="object" class="oe_highlight" invisible="state != 'draft'"/>
                    <field name="state" widget="statusbar" statusbar_visible="draft,progress,done"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1>
                            <field name="name" placeholder="Task title..."/>
                        </h1>
                    </div>
                    <group>
                        <group name="left_details">
                            <field name="partner_id" readonly="state == 'done'"/>
                            <field name="company_id" readonly="state == 'done'"/>
                        </group>
                        <group name="right_metrics">
                            <field name="estimated_hours" readonly="state == 'done'"/>
                            <field name="discount_rate" readonly="state == 'done'" required="estimated_hours > 10"/>
                            <field name="cost_total"/>
                        </group>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <record id="project_task_optimizer_action" model="ir.actions.act_window">
        <field name="name">Performance Analysis</field>
        <field name="res_model">project.task.optimizer</field>
        <field name="view_mode">list,form</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Create your first sales performance analysis.
            </p>
        </field>
    </record>
</odoo>
```

### 5. Isolated Navigation Menu Structure: `views/sales_performance_menus.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <menuitem id="menu_sales_performance_root"
              name="Performance Analysis"
              parent="sale.menu_sale_config"
              sequence="50"/>

    <menuitem id="menu_sales_performance_optimizer"
              name="Analysis Tasks"
              parent="menu_sales_performance_root"
              action="project_task_optimizer_action"
              sequence="10"/>
</odoo>