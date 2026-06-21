# Odoo 18 & 19 XML View and Menu Standards

Ensure all XML declarations meet modern Odoo 19.0 specifications.

## 1. tree vs list root tags (v18+)

The classic `<tree>` root tag is completely obsolete and removed in Odoo 18. Any list view must use `<list>`:

```xml
<!-- GOOD -->
<record id="my_model_view_list" model="ir.ui.view">
    <field name="name">my.model.view.list</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <list string="My Records">
            <field name="name"/>
        </list>
    </field>
</record>
```

## 2. Dynamic visibility inline (v17+)

Dictionary-styled `attrs` are obsolete. Define attributes inline:

```xml
<!-- GOOD -->
<field name="partner_id" invisible="state == 'draft'" readonly="state == 'done'" required="state == 'progress'"/>
```

## 3. Menu Separation

To prevent cyclical install errors, isolate all parent/child `<menuitem>` tags inside `views/<module_name>_menus.xml`.\n