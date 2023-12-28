# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api, _
from datetime import datetime, date
import calendar
class ClassificationsReortWizard(models.TransientModel):
    _name = 'classification.report.wizard'
    _description = 'classification.report.wizard'
    start_date = fields.Date(
        string='Date From',
        required=True)
    end_date = fields.Date(
        string='Date To',
        required=True)

    @api.model
    def default_get(self, fields):
        res = super(ClassificationsReortWizard, self).default_get(fields)
        month = date.today().month
        year = date.today().year
        start_date = date(year, month, 1)
        result = calendar.monthrange(start_date.year, start_date.month)
        last_day = result[1]
        end_date = date(year, month, last_day)
        res['start_date'] = start_date
        res['end_date'] = end_date

        return res

    def _get_date_domain(self):
        month = self.start_date.month
        year = self.start_date.year
        day = self.start_date.day
        start_date = datetime(year, month, day, 0, 0, 0)
        month2 = self.end_date.month
        year2 = self.end_date.year
        day2 = self.end_date.day
        end_date = datetime(year2, month2, day2, 11, 59, 59)
        domain = [('date_order', '>=', start_date), ('date_order', '<=', end_date)]
        return domain

    def create_zero_warehouses(self,warehouses, classification_month):
        zero_list_ids = []
        zero_list = []
        for warehouse in warehouses:
            vals_dict = {'warehouse_id': warehouse.id,
                         'total_sales': 0.0,
                         'total_refund': 0.0,
                         'total': 0.0
                         }
            target = self.get_target_amount(warehouse)
            if target:
                vals_dict['target'] = target
                percentage = 0.0
                vals_dict['percentage'] = percentage
            else:
                vals_dict['target'] = 0.0
                vals_dict['percentage'] = 0.0
            classification = self._get_classification(vals_dict['percentage'])
            # if vals_dict['percentage'] > 100:
            #     classification = self.get_over_hendred_classification(percentage)
            vals_dict['classification'] = classification
            vals_dict['classification_month'] = classification_month
            classification = self.env['branches.classification'].sudo().create(vals_dict)
            zero_list_ids.append(classification.id)
            vals_dict['name'] = warehouse.name
            zero_list.append(vals_dict)
        return zero_list, zero_list_ids

    def _get_warehouses_data(self):
        domain = self._get_date_domain()
        orders = self.env['pos.order'].sudo().search(domain)
        orders = orders.filtered(lambda order: order.state in ['paid', 'done', 'invoiced'])
        group_dict = {}
        for order in orders:
            if order.config_id.picking_type_id.warehouse_id not in group_dict.keys():
                group_dict[order.config_id.picking_type_id.warehouse_id] = [order]
            else:
                group_dict[order.config_id.picking_type_id.warehouse_id].append(order)
        return group_dict

    def action_calculate_classification(self):
        warehouses_data = self._get_warehouses_data()
        vals_list = []
        ware_houses_ids = [ware.id for ware in warehouses_data.keys()]
        ids_list = []
        not_existed_warehouses = self.env['stock.warehouse'].sudo().search([('id', 'not in', ware_houses_ids)])
        month = self.start_date.month
        year = self.start_date.year
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
            classification = self._get_classification(vals_dict['percentage'])
            # if vals_dict['percentage'] > 100:
            #     classification = self.get_over_hendred_classification(percentage)
            vals_dict['classification'] = classification
            vals_dict['classification_month'] = classification_month
            vals_list.append(vals_dict)
            classification = self.env['branches.classification'].sudo().create(vals_dict)
            ids_list.append(classification.id)
        zero_list_ids = self.create_zero_warehouses(not_existed_warehouses, classification_month)[1]
        all_list =zero_list_ids + ids_list
        action = {
            'name': _("Branches Classification"),
            'type': 'ir.actions.act_window',
            'res_model': 'branches.classification',
            'view_mode': 'list',
            'domain': [('id', 'in', all_list)],

        }

        return action

    def get_target_amount(self, warehouse):
        target_line = self.env['warehouses.target'].sudo().search([('warehouse_id', '=', warehouse.id)], limit=1)
        if target_line and target_line.target > 0:
            return target_line[-1].target
        else:
            return False

    def _get_classification(self, percent):
        percent = round(percent, 2)
        classes = self.env['warehouses.class'].sudo().search([])
        name = ''
        for cla in classes:
            if percent == cla.percent_to:
                name = cla.name
                break
        class_line = classes.filtered(lambda c: c.percent_from <= percent <= c.percent_to)
        if class_line:
            name = class_line[-1].name
        else:
            name = 'No Class Defined'
        return name

    def get_over_hendred_classification(self, percentage):
        classes = self.env['warehouses.class'].sudo().search([('percent_to', '=', 100)])
        if classes:
            return classes[-1].name
        else:
            return 'No Class Defined'

    def action_print_pdf(self):
        data = {}
        data['form'] = self.read()[0]
        return self.env.ref('point_of_sale_valuation.action_report_classification_pdf').report_action(self, data=None)

    def get_report_pdf_data(self):
        warehouses_data = self._get_warehouses_data()
        vals_list = []
        ids_list = []
        month = self.start_date.month
        year = self.start_date.year
        classification_month = str(month) + ' - ' + str(year)
        ware_houses_ids = [ware.id for ware in warehouses_data.keys()]

        not_existed_warehouses = self.env['stock.warehouse'].sudo().search([('id', 'not in', ware_houses_ids)])

        for warehouse, orders in warehouses_data.items():
            vals_dict = {'warehouse_id': warehouse.id}
            total_sales = 0.0
            total_refund = 0.0
            for order in orders:
                if order.amount_total > 0:
                    total_sales += order.amount_total
                elif order.amount_total < 0:
                    total_refund += order.amount_total
            vals_dict['total_sales'] = round(total_sales,2)
            vals_dict['total_refund'] = round(total_refund,2)
            vals_dict['total'] = round(total_sales + total_refund,2)
            target = self.get_target_amount(warehouse)
            if target:
                vals_dict['target'] = round(target, 2)
                percentage = ((total_sales + total_refund) / target) * 100
                vals_dict['percentage'] = round(percentage, 2)
            else:
                vals_dict['target'] = 0.0
                vals_dict['percentage'] = 100
            classification = self._get_classification(vals_dict['percentage'])
            # if vals_dict['percentage'] > 100:
            #     classification = self.get_over_hendred_classification(percentage)
            vals_dict['classification'] = classification
            vals_dict['classification_month'] = classification_month
            classification = self.env['branches.classification'].sudo().create(vals_dict)
            vals_dict['name'] = warehouse.name
            vals_list.append(vals_dict)
        zero_list = self.create_zero_warehouses(not_existed_warehouses, classification_month)[0]
        all_list = vals_list + zero_list
        return all_list