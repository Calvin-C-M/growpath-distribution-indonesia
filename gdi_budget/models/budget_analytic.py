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
    
    @api.depends('account_account_id', 'account_id', 'date_from')
    def _compute_code(self):
        analytic_plans = self.env['account.analytic.plan'].search([])

        for rec in self:
            prefix = 'WBS'
            name = f"{prefix}"

            if rec.account_id:
                analytic_account = rec.account_id.code
                if analytic_account:
                    name += f"_{analytic_account}"

            for plan in analytic_plans:
                field_name = f'x_plan{plan.id}_id'
                if hasattr(rec, field_name):
                    plan_value = getattr(rec, field_name)
                    if plan_value:
                        name += f"_{plan_value.code}"


            if rec.date_from:
                month = rec.date_from.strftime('%b').upper()
                name += f"_{month}"

            if rec.account_account_id:
                name += f"_{rec.account_account_id.code}"

            rec.code = name

    @api.constrains('account_account_id')
    def _check_account_account_id(self):
        analytic_plans = self.env['account.analytic.plan'].search([])
        for rec in self:
            domain = [
                ('id', '!=', rec.id),
                ('account_account_id', '=', rec.account_account_id.id),
                ('account_id', '=', rec.account_id.id),
                ('date_from', '<=', rec.date_from),
                ('date_to', '>=', rec.date_from),
            ]

            # Dynamically add all analytic plan fields
            for plan in analytic_plans:
                field_name = f'x_plan{plan.id}_id'
                if hasattr(rec, field_name):
                    plan_value = getattr(rec, field_name)
                    if plan_value:
                        domain.append((field_name, '=', plan_value.id))

            other_budget_lines = self.search(domain)
            if other_budget_lines:
                raise ValidationError(
                    "Budget line with the same account, analytic plan(s), and overlapping date range already exists."
                )