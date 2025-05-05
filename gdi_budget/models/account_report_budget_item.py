from odoo import api, models, fields
from datetime import date


class AccountReportBudgetItem(models.Model):
    _name = 'account.report.budget.item'
    _inherit = ['account.report.budget.item', 'analytic.mixin']

    name = fields.Char(string='Budget Code', compute="_compute_code", help='Budget code identifier')
    accumulated_amount = fields.Float(string='Accumulated Amount', compute="_compute_accumulated_amount", store=True, help='Accumulated amount for the budget item')

    @api.depends('date')
    def _compute_code(self):
        for rec in self:
            prefix = 'WBS'
            month = date(1990, rec.date.month, 1).strftime('%b').upper()
            account_code = rec.account_id.code
            analytic_account = rec.distribution_analytic_account_ids[0] if rec.distribution_analytic_account_ids else None
            
            if analytic_account:
                rec.name = f"{prefix}_{analytic_account.name}_{month}_{account_code}"
            else:
                rec.name = f"{prefix}_{month}_{account_code}"

    @api.depends('amount')
    def _compute_accumulated_amount(self):
        for rec in self:
            po_lines = self.env['purchase.order.line'].search([
                ('budget_id', '=', rec.id),
            ])
            rec.accumulated_amount = sum(po_lines.mapped('price_subtotal'))
