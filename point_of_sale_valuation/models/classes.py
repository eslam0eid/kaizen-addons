# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api, _


class WarehousesClass(models.Model):
    _name = 'warehouses.class'
    _description = 'WarehousesClass'

    name = fields.Char(
        string='Class',
        required=True)
    percent_from = fields.Float(
        string='From(%)',
        required=False)
    percent_to = fields.Float(
        string='To(%)',
        required=False)

    @api.constrains('percent_from', 'percent_to')
    def _restrict_amounts(self):
        if self.percent_from >= self.percent_to:
            raise ValidationError(_('Percent from must be less than percent to.'))

    @api.model
    def create(self, vals):
        classes = self.env['warehouses.class'].sudo().search([])
        from_list = classes.mapped('percent_from')
        to_list = classes.mapped('percent_to')
        ranges = zip(from_list, to_list)
        current_range = (vals['percent_from'], vals['percent_to'])
        if current_range in ranges:
            raise ValidationError(_('Classification already exists'))
        for ware_class in classes:
            if ware_class.percent_from < vals['percent_from'] < ware_class.percent_to or ware_class.percent_from < vals['percent_to'] < ware_class.percent_to:
                raise ValidationError(_('Intersection between Classifications is not allowed '))
        for ware in classes:
            if ware.percent_from >= vals['percent_from'] and ware.percent_to <= vals['percent_to']:
                raise ValidationError(_('Intersection between Classifications is not allowed'))

        res = super(WarehousesClass, self).create(vals)
        return res

    def write(self, values):
        res = super(WarehousesClass, self).write(values)
        classes = self.env['warehouses.class'].sudo().search([('id', '!=', self.id)])
        from_list = classes.mapped('percent_from')
        to_list = classes.mapped('percent_to')
        ranges = zip(from_list, to_list)
        current_range = (self.percent_from, self.percent_to)
        if current_range in ranges:
            raise ValidationError(_('Classification already exists'))
        for ware_class in classes:
            if ware_class.percent_from < self.percent_from < ware_class.percent_to or ware_class.percent_from < self.percent_to < ware_class.percent_to:
                raise ValidationError(_('Intersection between Classifications is not allowed'))
        for ware in classes:
            if ware.percent_from >= self.percent_from and ware.percent_to <= self.percent_to:
                raise ValidationError(_('Intersection between Classifications is not allowed'))

        return res