# -*- coding: utf-8 -*-
{
    'name': "Internal Transfer Product Block",

    'summary': """
      Block product from internal transfer, internal transfer product block, block variant for internal transfer, 
      products internal transfer, variants internal transfer,prevent product from internal transfer""",

    'description': """
       Block product from internal transfer, internal transfer product block, block variant for internal transfer, 
        products internal transfer, variants internal transfer,prevent product from internal transfer
    """,

     'author': "Kaizen Principles",
    'website': 'https://erp-software.odoo-saudi.com/discount/',

    'category': 'Stock',
    'version': '17.0.0.0.1',
    'license': 'OPL-1',


    'depends': ['base', 'stock', 'product'],

    # always loaded
    'data': [
        'views/product_template_view.xml',
    ],
    # only loaded in demonstration mode
    'images': ['static/description/banner.gif'],
    'installable': True,
    'auto_install': False,


}
