# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api, _
from datetime import datetime, date
import calendar


class BranchesClassifications(models.TransientModel):
    _name = 'branches.classification'
    _description = 'BranchesClassification'
    _rec_name = 'warehouse_id'

    warehouse_id = fields.Many2one(
        comodel_name='stock.warehouse',
        string='Branch',
        required=True)
    total_sales = fields.Float(
        string='Total Sales',
        required=False)
    total_refund = fields.Float(
        string='Total Refund',
        required=False)
    total = fields.Float(
        string='Total',
        required=False)
    target = fields.Float(
        string='Target',
        )
    percentage = fields.Float(
        string='Percent(%)',
        required=False)
    classification = fields.Char(
        string='Classification',
        required=False)
    classification_month = fields.Char(
        string='Classification Month',
        required=False)

    def _get_date_domain(self):
        month = date.today().month
        year = date.today().year
        start_date = datetime(year, month, 1, 0, 0, 0)

        res = calendar.monthrange(start_date.year, start_date.month)
        last_day = res[1]
        end_date = datetime(year, month, last_day, 11, 59, 59)
        domain = [('date_order', '>=', start_date), ('date_order', '<=', end_date)]
        return domain

    def _get_warehouses_data(self):
        domain = self._get_date_domain()
        orders = self.env['pos.order'].sudo().search(domain)
        orders = orders.filtered(lambda order: order.state == 'paid')
        group_dict = {}
        for order in orders:
            # print(order.config_id.picking_type_id.warehouse_id.name)
            if order.config_id.picking_type_id.warehouse_id not in group_dict.keys():
                group_dict[order.config_id.picking_type_id.warehouse_id] = [order]
            else:
                group_dict[order.config_id.picking_type_id.warehouse_id].append(order)
        return group_dict

    def pprit_data(self):
        pass

    def action_calculate_classification(self):
        warehouses_data = self._get_warehouses_data()
        vals_list = []
        month = date.today().month
        year = date.today().year
        classification_month = str(month) + ' - ' + str(year)
        for warehouse, orders in warehouses_data.items():
            vals_dict = {'warehouse_id': warehouse.id}
            total_sales = 0.0
            total_refund = 0.0
            for order in orders:
                if order.amount_total > 0:
                    total_sales += order.amount_total
                elif order.amount_total < 0:
                    total_refund += order.amount_total
            vals_dict['total_sales'] = total_sales
            vals_dict['total_refund'] = total_refund
            vals_dict['total'] = total_sales + total_refund
            target = self.get_target_amount(warehouse)
            if target:
                vals_dict['target'] = target
                percentage = ((total_sales + total_refund) / target) * 100
                vals_dict['percentage'] = percentage
            else:
                vals_dict['target'] = 0.0
                vals_dict['percentage'] = 100
            classification = self._get_classification(percentage)
            vals_dict['classification'] = classification
            vals_dict['classification_month'] = classification_month
            vals_list.append(vals_dict)
            self.sudo().create(vals_dict)

    def get_target_amount(self, warehouse):
        target_line = self.env['warehouses.target'].sudo().search([('warehouse_id', '=', warehouse.id)], limit=1)
        if target_line and target_line.target > 0:
            return target_line.target
        else:
            return False

    def _get_classification(self, percent):
        classes = self.env['warehouses.class'].sudo().search([])
        class_line = classes.filtered(lambda c: c.percent_from <= percent <= c.percent_to)
        if class_line:
            return class_line.name
        else:
            return 'No Class Defined'




