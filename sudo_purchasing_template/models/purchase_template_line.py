from odoo import api, fields, models


class PurchaseOrderTemplateLine(models.Model):
    _name = 'purchase.template.line'
    _inherit = 'analytic.mixin'

    name = fields.Char(string='Description', required=True)
    product_id = fields.Many2one(comodel_name='product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity')
    uom_id = fields.Many2one(comodel_name='uom.uom', string='Unit of Measure',
                             domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_po_id.category_id')
    template_id = fields.Many2one(comodel_name='purchase.template', string='Template')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self._get_product_purchase_description(self.product_id)
            self.uom_id = self.product_id.uom_po_id or self.product_id.uom_id

    def _get_product_purchase_description(self, product):
        name = product.display_name
        if product.description_purchase:
            name += '\n' + product.description_purchase
        return name
