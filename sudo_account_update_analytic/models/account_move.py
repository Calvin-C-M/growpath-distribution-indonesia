from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_launch_update_analytic_account(self):
        return {
            'name': 'Update Analytic Account',
            'type': 'ir.actions.act_window',
            'res_model': 'update.analytic.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_ids': self.line_ids.ids
            }
        }
