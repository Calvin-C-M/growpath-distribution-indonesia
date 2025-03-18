from odoo import api, fields, models


class PurchaseOrderTemplate(models.Model):
    _name = 'purchase.template'
    _description = 'Template for creating purchase order lines'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    template_type = fields.Selection(string='Template Type', selection=[
        ('order', 'Purchase Order Template'),
        ('request', 'Purchase Request Template')
    ], default='order')
    product_line_ids = fields.One2many(comodel_name='purchase.template.line', inverse_name='template_id', string='Product Lines')
