from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    _sql_constraints = [
        ('phone_unique', 'unique (phone)', "Phone number already exists!"),
    ]
