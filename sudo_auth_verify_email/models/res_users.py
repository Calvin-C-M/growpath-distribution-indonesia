from odoo import api, fields, models, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _signup_create_user(self, values):
        if self._get_signup_invitation_scope() == 'b2c_verify':
            return self._create_user_from_template(values)
        return super(ResUsers, self)._signup_create_user(values)
