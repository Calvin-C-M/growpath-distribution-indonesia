from odoo import api, fields, models


class ConfirmUpdateAnalyticWizard(models.TransientModel):
    _name = 'confirm.update.analytic.wizard'

    def action_confirm(self):
        move_line_id = self.env['account.move.line'].browse(self.env.context.get('active_ids'))
        analytic_distribution = self.env.context.get('analytic_distribution')

        move_line_id.write({
            'analytic_distribution': analytic_distribution
        })
