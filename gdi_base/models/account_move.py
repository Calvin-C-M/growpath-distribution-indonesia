from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.depends('posted_before', 'state', 'journal_id', 'date', 'move_type', 'origin_payment_id')
    def _compute_name(self):
        self = self.sorted(lambda m: (m.date, m.ref or '', m._origin.id))

        for move in self:
            if move.move_type == 'out_invoice':
                move.name = self.env['ir.sequence'].next_by_code('account.move.invoice') or '/'
            elif move.move_type == 'in_invoice':
                move.name = self.env['ir.sequence'].next_by_code('account.move.vendor.bill') or '/'
            else:
                if move.state == 'cancel':
                    continue

                move_has_name = move.name and move.name != '/'
                if not move.posted_before and not move._sequence_matches_date():
                    # The name does not match the date and the move is not the first in the period:
                    # Reset to draft
                    move.name = False
                    continue
                if move.date and not move_has_name and move.state != 'draft':
                    move._set_next_sequence()
                    
        self._inverse_name()
