from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _get_product_domain(self):
        return [('purchase_ok', '=', True), ('categ_id', '=', self.product_category_id.id)]

    product_category_id = fields.Many2one(
        'product.category', string='Product, Category', related='product_id.product_tmpl_id.categ_id'
    )
    account_id = fields.Many2one(
        'account.account', string='Chart of Account', related='product_category_id.property_account_expense_categ_id'
    )
    # product_id = fields.Many2one(domain=_get_product_domain)
    product_id = fields.Many2one(domain=lambda self: [('purchase_ok', '=', True), ('categ_id', '=', self.product_category_id.id)])

    # @api.onchange('product_category_id')
    # def _onchange_product_category_id(self):
    #     if self.product_category_id:
    #         return {
    #             'domain': {
    #                 'product_id': [('purchase_ok', '=', True), ('categ_id', '=', self.product_category_id.id)]
    #             }
    #         }
    #     else:
    #         return {
    #             'domain': {
    #                 'product_id': []
    #             }
    #         }
