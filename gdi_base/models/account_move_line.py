from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.constrains('quantity', 'purchase_line_id')
    def _validate_quantity(self):
        if self.purchase_line_id and self.quantity > self.purchase_line_id.product_qty:
            raise ValidationError('Quantity cannot be greater than demand quantity')
        
    @api.constrains('move_id')
    def _validate_purchase_lines(self):
        if self in self.move_id.invoice_line_ids:
            source_orders = self.move_id.invoice_line_ids.mapped('purchase_order_id')
            if source_orders and not self.purchase_line_id:
                raise ValidationError('Purchase line must be part of the purchase order')

    @api.constrains('move_id')
    def _validate_sale_lines(self):
        if self in self.move_id.invoice_line_ids:
            source_orders = self.move_id.invoice_line_ids.sale_line_ids.order_id
            if source_orders and not self.purchase_line_id:
                raise ValidationError('Sale line must be part of the purchase order')
        