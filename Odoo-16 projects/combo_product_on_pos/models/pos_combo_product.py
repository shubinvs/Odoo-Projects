from odoo import fields, models, api


class PosComboProduct(models.Model):
    _name = 'pos.combo.product'

    product_id = fields.Many2one('product.product')
    category_id = fields.Many2one('pos.category')
    product_ids = fields.Many2many('product.product',
                                   domain="[('pos_categ_id', '=', category_id)]")
    is_required = fields.Boolean(string="Is Required")
    item_count = fields.Integer(string="Item Count")


class ProductTemplate(models.Model):
    _inherit = 'product.product'

    is_combo = fields.Boolean(string="Is Combo")
    combo_ids = fields.One2many('pos.combo.product', 'product_id')

    @api.onchange('combo_ids')
    def _item_count(self):
        count = 0
        for rec in self.combo_ids:
            for i in rec.product_ids:
                count += 1
            rec.item_count = count
            count = 0

    @api.model
    def get_product_details(self, combo_product):
        combo_products = self.env['product.product'].browse(combo_product)
        products = []
        for cat in combo_products.combo_ids:
            inner_product = []
            product_dict = {}
            product_dict['category_name'] = cat.category_id.name
            for product in cat.product_ids:
                inner_product.append(
                    {'product_id': product.id, 'product_name': product.name,
                     'count': cat.item_count, 'required': cat.is_required})
            product_dict['product'] = inner_product
            products.append(product_dict)
        print(products)
        return products
