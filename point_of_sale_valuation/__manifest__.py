# -*- coding: utf-8 -*-
{
    'name': "Points of Sale Valuation",

    'summary': """
        Point of sale valuation, point of sale classification, point of sale targets, point of sale valuation report, valuate your points of sale""" ,

    'description': """
           Point of sale valuation, point of sale classification, point of sale targets, point of sale valuation report, valuate my points of sale """ ,



    'author': "Kaizen Principles",
    'website': 'https://erp-software.odoo-saudi.com/discount/',

    'category': 'Point of Sale',
    'version': '17.0.0.1',
    'license': 'OPL-1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'point_of_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/classes.xml',
        'wizard/classification_wizard_report.xml',
        'views/warehouse_target.xml',
        'views/warehouses_classificaion.xml',
        'reports/branches_classification_report.xml'

    ],
    'images': ['static/description/banner.gif'],
    'installable': True,
    'auto_install': False,

}



