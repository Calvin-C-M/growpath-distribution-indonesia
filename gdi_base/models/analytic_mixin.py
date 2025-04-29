from odoo import api, fields, models


class AnalyticMixin(models.AbstractModel):
    _inherit = 'analytic.mixin'

    analytic_distribution = fields.Json(string='Call Center')

