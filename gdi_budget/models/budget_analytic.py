from odoo import api, fields, models
from odoo.exceptions import ValidationError

class BudgetLine(models.Model):
    _inherit = 'budget.line'

    _rec_name = 'code'

    code = fields.Char(string='Budget Code', compute='_compute_code', store=True)
    account_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Chart of Accounts',
        help='Account linked to this budget item.',
    )
    
    achieved_amount = fields.Monetary(store=True)
    achieved_percentage = fields.Float(store=True)
    committed_amount = fields.Monetary(store=True)
    committed_percentage = fields.Float(store=True)

    @api.depends('account_account_id', 'account_id', 'date_from')
    def _compute_code(self):
        for rec in self:
            prefix = 'WBS'
            name = f"{prefix}"

            if rec.account_id:
                analytic_account = rec.account_id.name
                if analytic_account:
                    name += f"_{analytic_account}"

            if rec.date_from:
                month = rec.date_from.strftime('%b').upper()
                name += f"_{month}"

            if rec.account_account_id:
                name += f"_{rec.account_account_id.code}"

            rec.code = name

    @api.constrains('account_account_id')
    def _check_account_account_id(self):
        for rec in self:
            other_budget_lines = self.search([
                ('id', '!=', rec.id),
                ('account_account_id', '=', rec.account_account_id.id),
                ('account_id', '=', rec.account_id.id),
                ('date_from', '<=', rec.date_from),
                ('date_to', '>=', rec.date_from),
            ])
            if other_budget_lines:
                raise ValidationError(
                    f"Budget line with the same account and date range already exists"
                )
