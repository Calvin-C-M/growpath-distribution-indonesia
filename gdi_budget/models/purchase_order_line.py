from odoo import api, fields, models
from datetime import datetime


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    budget_id = fields.Many2one(
        comodel_name="account.report.budget.item",
        string="Budget",
        compute="_compute_budget_id",
        store=True,
        help="Budget linked to this purchase order.",
    )

    @api.depends("distribution_analytic_account_ids")
    def _compute_budget_id(self):
        for line in self:
            if line.distribution_analytic_account_ids:
                analytic_distribution_id = line.distribution_analytic_account_ids[0]
                dt = fields.Datetime.to_datetime(line.date_order)
                month_start = dt.replace(day=1)

                # Calculate the first day of the next month
                if dt.month == 12:
                    next_month = dt.replace(year=dt.year + 1, month=1, day=1)
                else:
                    next_month = dt.replace(month=dt.month + 1, day=1)

                line.budget_id = self.env['account.report.budget.item'].search([
                    ('distribution_analytic_account_ids', 'in', [analytic_distribution_id.id]),
                    # Month domain
                    ('date', '>=', month_start.date()),
                    ('date', '<', next_month.date()),
                ], limit=1).id

