# -*- coding: utf-8 -*-
{
    'name': "Invoice Manual Currency Rate",

    'summary': """
       Invoice manual currency rate, currency manual rate in invoice, manual rate""",

    'description': """
        Invoice manual currency rate, currency manual rate in invoice, manual rate
    """,

    'author': "Kaizen Principles",
    'website': 'https://erp-software.odoo-saudi.com/discount/',

    'category': 'Accounting',
    'version': '0.1',
    'license': 'OPL-1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [

        'views/views.xml',
        'views/templates.xml',
    ],

    'images': ['static/description/banner.gif'],
    'installable': True,
    'auto_install': False,
    
}
