# -*- coding: utf-8 -*-
{
    "name": "Sales Performance Optimizer (OCA Standard)",
    "summary": "Advanced metrics and analytics for sales team targets",
    "version": "18.0.1.0.0", # Strict OCA SemVer format
    "category": "Sales",
    "author": "CTiEG",
    "license": "LGPL-3",
    "website": "https://www.ctieg.com",
    "depends": [
        "sale_management",
        "mail"
    ],
    # Dynamic conditional dependencies
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
}\n