# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    short_code = fields.Char(
        string='Short Code',
        required=False)

    generate_automatic_product_barcode = fields.Boolean(
        string='Generate Automatic Product Barcode',
        required=False)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    generate_automatic_product_barcode = fields.Boolean(
        string='Generate Automatic Product Barcode',
        readonly=False,related='company_id.generate_automatic_product_barcode')


class ProductCategory(models.Model):
    _inherit = 'product.category'

    short_code = fields.Char('Short Code')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, vals):
        res = super(ProductProduct,self).create(vals)
        config_line = self.env['product.barcode.configuration'].sudo().search([], limit=1)
        suffix = ''
        if config_line:
            if config_line.suffixs:
                suffix += config_line.suffixs
            if config_line.include_company_short_code:
                if self.env.company.short_code:
                    suffix += self.env.company.short_code
            if config_line.include_category_short_code:
                if res.categ_id:
                    if res.categ_id.short_code:
                        suffix += res.categ_id.short_code
            if config_line.include_template_barcode:
                if res.product_tmpl_id:
                    if res.product_tmpl_id.barcode:
                        suffix += res.product_tmpl_id.barcode

        sequence = self.env.ref('product_automatic_barcode.automatic_barcode_sequence')
        sequence.prefix = suffix
        res.barcode = self.env['ir.sequence'].next_by_code('product.automatic.barcode.sequence') or ('')
        return res




