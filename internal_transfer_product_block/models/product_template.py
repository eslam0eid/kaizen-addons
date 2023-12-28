# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Description'

    temp_is_blocked = fields.Boolean(string="Blocked The Product", store=True)
    temp_blocked_wherehouse_ids = fields.Many2many(comodel_name="stock.warehouse", string="Blocked Wherehouses", )
    temp_block_note = fields.Char(
        string='Note', 
        required=False, default ='Blocking this product template will block all its variants', readonly=1)
    temp_warehouse_note = fields.Char(
        string='',
        required=False,  readonly=1, default='Empty blocked warehouses value means blocking from all warehouses')

class ProductProduct(models.Model):
    _inherit = 'product.product'

    prod_blocked_wherehouse = fields.Many2many(comodel_name="stock.warehouse", string="Blocked Wherehouse",
                                          store=True, readonly=False)

    prod_is_blocked = fields.Boolean(string="Product Blocked", store=True,)



