from odoo import api, fields, models


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    is_downpayment_required = fields.Boolean(string='Require Downpayment?', default=False)
