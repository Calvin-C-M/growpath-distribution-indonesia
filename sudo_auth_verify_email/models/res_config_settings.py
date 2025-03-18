from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    auth_signup_uninvited = fields.Selection(selection_add=[
        ('b2c_verify', 'Verify Email'),
    ])
