from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_so(self):
        source_orders = self.line_ids.sale_line_ids.order_id
        if source_orders:
            return source_orders[0]
        else:
            return False
