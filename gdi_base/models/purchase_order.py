from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_downpayment_required = fields.Boolean(string='Require Downpayment?', default=False)
