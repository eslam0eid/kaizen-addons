# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class StockQuantityHistory(models.TransientModel):
    _inherit = 'stock.quantity.history'


    valuation_report = fields.Boolean(
        string='valuation_report',
        required=False)

    @api.model
    def default_get(self, fields):
        res = super(StockQuantityHistory, self).default_get(fields)
        active_model = self.env.context.get('active_model')
        if active_model == 'stock.valuation.layer':
            res['valuation_report'] = True

        return res

    def get_report_data(self):
        data = self.env['stock.valuation.layer'].sudo().search([('create_date', '<=', self.inventory_datetime), ('product_id.type', '=', 'product')])
        return data

    def print_valuation_report(self):
        data = {}
        data['form'] = self.read()[0]
        return self.env.ref('invetort_valuation_report.stock_inventory_valuation_report').report_action(self, data=None)

    def _get_report_base_filename(self):
        return 'Inventory Valuation Report' + str(self.inventory_datetime.strftime('%Y-%m-%d %H:%M'))