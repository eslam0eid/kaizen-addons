# -*- coding: utf-8 -*-


from odoo import models, api, fields


class ProductBarcodeConfiguration(models.Model):
    _name = 'product.barcode.configuration'
    _description = 'barcode.configuration'
    _rec_name = 'suffixs'

    include_template_barcode = fields.Boolean(
        string='Include Template Barcode',
        required=False)

    include_company_short_code = fields.Boolean(
        string='Include Company Short Code',
        required=False)

    include_category_short_code = fields.Boolean(
        string='Include Company Short Code',
        required=False)

    suffixs = fields.Char(
        string='Prefix',
        required=False)

    def apply(self):
        return True

    @api.model
    def get_config(self):
        return self.env.ref('product_automatic_barcode.default_barcode_configuration')
