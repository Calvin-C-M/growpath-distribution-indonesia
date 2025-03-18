from odoo import api, fields, models


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'
    
    purchase_template_id = fields.Many2one(comodel_name='purchase.template', string='Purchase Request Template',
                                           domain=[('template_type', '=', 'request')])

    @api.onchange('purchase_template_id')
    def _onchange_template(self):
        if self.purchase_template_id:
            self.line_ids = [(5, 0, 0)]
            for line in self.purchase_template_id.product_line_ids:
                self.line_ids = [(0, 0, {
                    'name': line.name,
                    'product_id': line.product_id.id,
                    'product_qty': line.quantity,
                    'product_uom_id': line.uom_id.id,
                    'analytic_distribution': line.analytic_distribution,
                })]
        return
