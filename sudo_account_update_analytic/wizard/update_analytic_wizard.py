from odoo import api, fields, models, _
from odoo.exceptions import UserError
import json


class UpdateAnalyticWizard(models.TransientModel):
    _name = 'update.analytic.wizard'
    _inherit = ['analytic.mixin']
    _description = 'Update Analytic Account'

    preview_analytic_distribution = fields.Json(string='Preview Analytic Distribution', readonly=True)
    move_line_ids = fields.Many2many(comodel_name='account.move.line')
    account_id = fields.Many2many(comodel_name='account.account', string='Chart of Accounts', required=True)

    @api.model
    def default_get(self, fields):
        res = super(UpdateAnalyticWizard, self).default_get(fields)

        if self.env.context.get('active_model') not in ['account.move.line', 'account.move'] or not self.env.context.get('active_ids'):
            raise UserError(_('This can only be used on journal items or entries'))

        move_line_ids = self.env['account.move.line'].browse(self.env.context['active_ids'])
        res['move_line_ids'] = [(6, 0, move_line_ids.ids)]

        res['account_id'] = [(6, 0, move_line_ids.account_id.ids)]

        move_line_analytic_distribution = move_line_ids.mapped('analytic_distribution')
        res['preview_analytic_distribution'] = {
            key: value
            for record in move_line_analytic_distribution if record
            for key, value in record.items()
        }

        return res

    def action_update_analytic_account(self):
        for move_line_id in self.move_line_ids:
            if move_line_id.account_id.id in self.account_id.ids:
                if move_line_id.analytic_distribution:
                    return {
                        'name': 'Update Analytic Account',
                        'type': 'ir.actions.act_window',
                        'res_model': 'confirm.update.analytic.wizard',
                        'view_mode': 'form',
                        'target': 'new',
                        'context': {
                            'active_ids': self.move_line_ids.ids,
                            'analytic_distribution': self.analytic_distribution
                        }
                    }
                move_line_id.analytic_distribution = self.analytic_distribution
