from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.depends('posted_before', 'state', 'journal_id', 'date', 'move_type', 'origin_payment_id')
    def _compute_name(self):
        self = self.sorted(lambda m: (m.date, m.ref or '', m._origin.id))

        for move in self:
            if move.state == 'cancel':
                continue

            move_has_name = move.name and move.name != '/'

            if move.move_type == 'out_invoice' and not move_has_name:
                sequence = self.env.ref('gdi_base.account_move_invoice')
                move.name = sequence.get_next_char(sequence.number_next_actual)
            elif move.move_type == 'in_invoice' and not move_has_name:
                sequence = self.env.ref('gdi_base.account_move_vendor_bill')
                move.name = sequence.get_next_char(sequence.number_next_actual)
            else:
                if not move.posted_before and not move._sequence_matches_date():
                    # The name does not match the date and the move is not the first in the period:
                    # Reset to draft
                    move.name = False
                    continue
                if move.date and not move_has_name and move.state != 'draft':
                    move._set_next_sequence()
                    
        self._inverse_name()
        
    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        excluded_move_types = ['in_invoice', 'out_invoice']
        if self.move_type not in excluded_move_types:
            super()._onchange_journal_id()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'name' in vals and 'move_type' in vals:
                if vals['move_type'] == 'out_invoice':
                    sequence = self.env.ref('gdi_base.account_move_invoice')
                    if vals['name'] == sequence.get_next_char(sequence.number_next_actual):
                        vals['name'] = self.env['ir.sequence'].next_by_code('account.move.invoice')
                elif vals['move_type'] == 'in_invoice':
                    sequence = self.env.ref('gdi_base.account_move_vendor_bill')
                    if vals['name'] == sequence.get_next_char(sequence.number_next_actual):
                        vals['name'] = self.env['ir.sequence'].next_by_code('account.move.vendor.bill')

        return super().create(vals_list)
        