from odoo import api, fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    code = fields.Char(
        size=50
    )

    # sequence_id = fields.Many2one(
    #     'ir.sequence',
    #     string='Sequence',
    #     help="The sequence used to generate the journal entries for this journal.",
    #     required=True,
    # )
    # sequence_code = fields.Char(
    #     string='Sequence Code',
    #     help="The code of the sequence used to generate the journal entries for this journal.",
    #     related='sequence_id.code',
    # )
    # sequence_prefix = fields.Char(
    #     string='Sequence Prefix',
    #     help="The code of the sequence used to generate the journal entries for this journal.",
    #     related='sequence_id.prefix',
    # )
