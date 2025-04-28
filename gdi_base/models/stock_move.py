from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.constrains('quantity', 'product_uom_qty')
    def _validate_demand_quantity(self):
        for rec in self:
            if rec.quantity > rec.product_uom_qty:
                raise ValidationError('Quantity cannot be greater than demand quantity')
        
    @api.constrains('picking_id')
    def _validate_picking_purchase_lines(self):
        for rec in self:
            if rec.picking_id.purchase_id:
                purchase_lines = rec.picking_id.purchase_id.order_line.ids
                if not rec.purchase_line_id or rec.purchase_line_id.id not in purchase_lines:
                    raise ValidationError('Purchase line must be part of the purchase order')
        
    @api.constrains('picking_id')
    def _validate_picking_sale_lines(self):
        for rec in self:
            if rec.picking_id.sale_id:
                sale_lines = rec.picking_id.sale_id.order_line.ids
                if not rec.sale_line_id or rec.sale_line_id.id not in sale_lines:
                    raise ValidationError('Sales line must be part of the purchase order')
