# -*- coding: utf-8 -*-
{
    'name': "Product Automatic Barcode",

    'summary': """
       Product Automatic Barcode Creation""",

    'description': """
        Product Automatic Barcode,Automatic Product barcode generation, generate automatic product barcode
    """,



    'author': "Kaizen Principles",
    'website': "https://erp-software.odoo-saudi.com/discount/",

    'category': 'Inventory',
    'version': '17.0.0.0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/barcode_config.xml',
        'data/sequence.xml',
        'views/barcode_config.xml',
        'views/company.xml',
        'views/category.xml',
        'views/res_config_settings.xml',
    ],

    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': False,

}

