from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def request_validation(self):
        for order in self:
            for line in order.order_line:
                if line.budget_line_id and line.is_above_budget:
                    raise ValidationError(
                        f"The selected limit is over budget of {line.budget_line_id.code}."
                    )

        return super().request_validation()
    
    def confirm_button(self):
        for order in self:
            for line in order.order_line:
                if line.budget_line_id and line.is_above_budget:
                    raise ValidationError(
                        f"The selected limit is over budget of {line.budget_line_id.code}."
                    )

        return super().confirm_button()
