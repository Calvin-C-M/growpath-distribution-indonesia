from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    budget_line_id = fields.Many2one(
        'budget.line',
        compute="_compute_budget_line_id",
        string='Budget Line',
        help='Budget line associated with the move line'
    )

    @api.depends('account_id', 'distribution_analytic_account_ids', 'date')
    def _compute_budget_line_id(self):
        for line in self:
            domain = [
                ('account_account_id', '=', line.account_id.id),
                ('date_from', '<=', line.date),
                ('date_to', '>=', line.date),
            ]

            if line.distribution_analytic_account_ids:
                domain.append(('account_id', '=', line.distribution_analytic_account_ids[0].id))

            budget_line = self.env['budget.line'].search(domain, limit=1)
            line.budget_line_id = budget_line.id if budget_line else False
