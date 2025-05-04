from odoo import api, models, fields
from datetime import date


class AccountReportBudgetItem(models.Model):
    _name = 'account.report.budget.item'
    _inherit = ['account.report.budget.item', 'analytic.mixin']

    code = fields.Char(string='Budget Code', compute="_compute_code", help='Budget code identifier')

    @api.depends('date')
    def _compute_code(self):
        for rec in self:
            prefix = 'WBS'
            month = date(1990, rec.date.month, 1).strftime('%b').upper()
            account_code = rec.account_id.code
            analytic_account = rec.distribution_analytic_account_ids[0] if rec.distribution_analytic_account_ids else None
            
            if analytic_account:
                rec.code = f"{prefix}_{analytic_account.name}_{month}_{account_code}"
            else:
                rec.code = f"{prefix}_{month}_{account_code}"
