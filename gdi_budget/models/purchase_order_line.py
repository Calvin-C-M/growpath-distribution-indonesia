from odoo import api, fields, models
from odoo.exceptions import ValidationError
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

    @api.constrains("budget_id")
    def _check_budget_id(self):
        for line in self:
            if line.budget_id and line.budget_id.amount < line.budget_id.accumulated_amount + line.price_subtotal:
                raise ValidationError(
                    f"The selected limit is over budget of {line.budget_id.name}."
                )

    @api.depends("distribution_analytic_account_ids", "price_subtotal")
    def _compute_budget_id(self):
        for line in self:
            if line.distribution_analytic_account_ids:
                analytic_distribution_id = line.distribution_analytic_account_ids[0]
                dt = fields.Datetime.to_datetime(line.date_order)
                month_start = dt.replace(day=1, month=1)
                # target_year = dt.year
                month_end = dt.replace(day=31, month=12)

                line.budget_id = self.env['account.report.budget.item'].search([
                    ('distribution_analytic_account_ids', 'in', [analytic_distribution_id.id]),
                    ('account_id', '=', line.account_id.id),
                    # Year domain
                    ('date', '>=', month_start.date()),
                    ('date', '<', month_end.date()),
                ], limit=1).id

