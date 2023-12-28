# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from functools import lru_cache


class AccountMove(models.Model):
    _inherit = 'account.move'

    manual_rate = fields.Float(
        string='Manual Currency Rate',
        required=False)
    apply_currency_rate = fields.Boolean(
        string='Apply Currency Rate',
        required=False)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.depends('currency_id', 'company_id', 'move_id.date', 'move_id.manual_rate')
    def _compute_currency_rate(self):
        @lru_cache()
        def get_rate(from_currency, to_currency, company, date):
            return self.env['res.currency']._get_conversion_rate(
                from_currency=from_currency,
                to_currency=to_currency,
                company=company,
                date=date,
            )

        for line in self:
            if line.move_id.manual_rate and line.move_id.apply_currency_rate:
                line.currency_rate = line.move_id.manual_rate
            line.currency_rate = get_rate(
                from_currency=line.company_currency_id,
                to_currency=line.currency_id,
                company=line.company_id,
                date=line.move_id.invoice_date or line.move_id.date or fields.Date.context_today(line),
            )
            print('line.currency_rate',line.currency_rate)

