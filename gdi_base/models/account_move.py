from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    # sequence_id = fields.Many2one(
    #     'ir.sequence',
    #     string='Sequence',
    #     related='journal_id.sequence_id',
    #     help="The sequence used to generate the journal entries for this journal.",
    # )
    
    # @api.constrains(lambda self: (self._sequence_field, self._sequence_date_field))
    # def _constrains_date_sequence(self):
    #     return True

    # @api.constrains('sequence_id')
    # def _check_sequence_id(self):
    #     for move in self:
    #         if not move.sequence_id:
    #             raise UserError(_('The sequence of the journal must be set.'))

    # @api.depends('posted_before', 'state', 'journal_id', 'date', 'move_type', 'origin_payment_id', 'sequence_id')
    # def _compute_name(self):
    #     self = self.sorted(lambda m: (m.date, m.ref or '', m._origin.id))

    #     for move in self:
    #         if move.state == 'cancel':
    #             continue
                
    #         move.name = move.sequence_id.get_next_char(move.sequence_id.number_next_actual) or '/'

    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         if 'name' in vals and 'journal_id' in vals:
    #             journal = self.env['account.journal'].browse(vals['journal_id'])
    #             if vals['name'] == journal.sequence_id.get_next_char(journal.sequence_id.number_next_actual):
    #                 vals['name'] = journal.sequence_id.next_by_code(journal.sequence_id.code)

    #     return super().create(vals_list)
        