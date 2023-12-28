# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api, _


class WarehousesTarget(models.Model):
    _name = 'warehouses.target'
    _description = 'WarehousesTarget'
    _rec_name = 'warehouse_id'

    warehouse_id = fields.Many2one(
        comodel_name='stock.warehouse',
        string='Warehouse',
        required=True)
    target = fields.Float(
        string='Target',
        required=True)

    _sql_constraints = [
        ('unique_warehouse_id', 'unique(warehouse_id)', 'This branch already exists.')]