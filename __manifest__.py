{
    "name": "App One",
    "author": "Shehab Saeed",
    "version": "17.0.0.1.0",
    "category": "",
    "depends": ["base", "sale_management", "mail", "contacts", "web"],
    "application": True,
    "license": "LGPL-3",
    "data": [
        "security/property_manager_group.xml",
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "views/base_menu.xml",
        "views/property_view.xml",
        "views/owner_view.xml",
        "views/tag_view.xml",
        "views/sale_order_view.xml",
        "views/res_partner_view.xml",
        "views/property_history_view.xml",
        "wizard/state_wizard_view.xml",
        "reports/property_report.xml"
    ],
    "assets": {
        'web.assets_backend':['app_one/static/src/css/property.css']
    }
}

