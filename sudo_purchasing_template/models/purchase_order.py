from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    purchase_template_id = fields.Many2one(comodel_name='purchase.template', string='Purchase Order Template',
                                           domain=[('template_type', '=', 'order')])

    @api.onchange('purchase_template_id')
    def _onchange_template(self):
        if self.purchase_template_id:
            self.order_line = [(5, 0, 0)]
            for line in self.purchase_template_id.product_line_ids:
                self.order_line = [(0, 0, {
                    'name': line.name,
                    'product_id': line.product_id.id,
                    'product_qty': line.quantity,
                    'product_uom': line.uom_id.id,
                    'analytic_distribution': line.analytic_distribution,
                })]
        return
