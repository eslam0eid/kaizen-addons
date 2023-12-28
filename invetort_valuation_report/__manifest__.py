# -*- coding: utf-8 -*-
{
    'name': "Inventory Valuation PDF Report",

    'summary': """
        Inventory Valuation Report pdf""",

    'description': """
        Inventory Valuation Report pdf
    """,

    'author': "Kaizen Principles",
    'website': "https://erp-software.odoo-saudi.com/discount/",

    'category': 'Inventory',
    'version': '17.0.0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock','account_accountant'],

    # always loaded
    'data': [
        'views/views.xml',
        'wizard/stock_quantity_history.xml',
        'wizard/report.xml',
    ],

    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': False,

}
