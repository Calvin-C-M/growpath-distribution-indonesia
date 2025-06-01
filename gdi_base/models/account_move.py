from odoo import api, fields, models, _
from odoo.exceptions import UserError
import calendar
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_starting_sequence(self):
        # EXTENDS account sequence.mixin
        self.ensure_one()
        move_date = self.date or self.invoice_date or fields.Date.context_today(self)
        year_part = "%04d" % move_date.year
        last_day = int(self.company_id.fiscalyear_last_day)
        last_month = int(self.company_id.fiscalyear_last_month)
        is_staggered_year = last_month != 12 or last_day != 31
        if is_staggered_year:
            max_last_day = calendar.monthrange(move_date.year, last_month)[1]
            last_day = min(last_day, max_last_day)
            if move_date > date(move_date.year, last_month, last_day):
                year_part = "%s-%s" % (move_date.strftime('%y'), (move_date + relativedelta(years=1)).strftime('%y'))
            else:
                year_part = "%s-%s" % ((move_date + relativedelta(years=-1)).strftime('%y'), move_date.strftime('%y'))
        # Arbitrarily use annual sequence for sales documents, but monthly
        # sequence for other documents
        if self.journal_id.type in ['sale', 'bank', 'cash', 'credit']:
            # We reduce short code to 4 characters (0000) in case of staggered
            # year to avoid too long sequences (see Indian GST rule 46(b) for
            # example). Note that it's already the case for monthly sequences.
            starting_sequence = "%s/%s/%s" % (self.journal_id.code, year_part, '000')
        else:
            starting_sequence = "%s/%s/%02d/000" % (self.journal_id.code, year_part, move_date.month)
        if self.journal_id.refund_sequence and self.move_type in ('out_refund', 'in_refund'):
            starting_sequence = "R" + starting_sequence
        if self.journal_id.payment_sequence and self.origin_payment_id or self.env.context.get('is_payment'):
            starting_sequence = "P" + starting_sequence
        return starting_sequence

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
        