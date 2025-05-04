from odoo import api, models, fields


class AccountReportBudgetItem(models.Model):
    _name = 'account.report.budget.item'
    _inherit = ['account.report.budget.item', 'analytic.mixin']
    