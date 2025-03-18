from odoo import api, fields, models


class Website(models.Model):
    _inherit = 'website'

    auth_signup_uninvited = fields.Selection(selection_add=[
        ('b2c_verify', 'Verify Email'),
    ])
