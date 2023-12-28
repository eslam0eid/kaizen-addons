# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.onchange('location_id', 'picking_type_id')
    def _onchange_location_blocked_products(self):
        if self.move_ids_without_package:
            if self.location_id and self.picking_type_id:
                for line in self.move_ids_without_package:
                    if self.picking_type_id.code == 'internal':
                        if line.product_id:
                            if line.product_id.product_tmpl_id.temp_is_blocked:
                                blocked_warehouses = line.product_id.product_tmpl_id.temp_blocked_wherehouse_ids.ids
                                if not blocked_warehouses:
                                    raise ValidationError(
                                        _("You can\'t add this product to internal transfer from %s" % self.location_id.display_name))
                                else:
                                    if self.location_id.warehouse_id.id in blocked_warehouses:
                                        raise ValidationError(
                                            _("You can\'t add this product to internal transfer from %s" % self.location_id.display_name))

                            if line.product_id.prod_is_blocked:
                                blocked_warehouses = line.product_id.prod_blocked_wherehouse.ids
                                if not blocked_warehouses:
                                    raise ValidationError(
                                        _("You can\'t add this product to internal transfer from %s" % self.location_id.display_name))
                                else:
                                    if self.location_id.warehouse_id.id in blocked_warehouses:
                                        raise ValidationError(
                                            _("You can\'t add this product to internal transfer from %s" % self.location_id.display_name))


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.onchange('product_id')
    def onchange_product_check_blocking(self):
        if not self.picking_type_id or not self.location_id:
            raise ValidationError(_("You must select operation type and source location"))
        if self.picking_type_id.code == 'internal':
            if self.product_id:
                if self.product_id.product_tmpl_id.temp_is_blocked:
                    blocked_warehouses = self.product_id.product_tmpl_id.temp_blocked_wherehouse_ids.ids
                    if not blocked_warehouses:
                        raise ValidationError(_("You can\'t add this product to internal transfer from %s"%self.location_id.display_name))
                    else:
                        if self.location_id.warehouse_id.id in blocked_warehouses:
                            raise ValidationError(_("You can\'t add this product to internal transfer from %s"%self.location_id.display_name))

                if self.product_id.prod_is_blocked:
                    blocked_warehouses = self.product_id.prod_blocked_wherehouse.ids
                    if not blocked_warehouses:
                        raise ValidationError(
                            _("You can\'t add this product to internal transfer from %s" % self.location_id.display_name))
                    else:
                        if self.location_id.warehouse_id.id in blocked_warehouses:
                            raise ValidationError(
                                _("You can\'t add this product to internal transfer from %s" % self.location_id.display_name))


