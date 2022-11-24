from odoo import models, fields, api


class Product(models.Model):
    _inherit = 'product.product'

    is_combo = fields.Boolean('Is Combo')
    combo_products_ids = fields.One2many('combo.product', 'combo_id')



class ComboProducts(models.Model):
    _name = 'combo.product'

    combo_id = fields.Many2one('product.product')
    category_id = fields.Many2one('product.category')
    product_id = fields.Many2many('product.product')
    is_required = fields.Boolean('Is Required')
    item_count = fields.Float('Item Count')

    @api.model
    def get_products(self, combo_product):
        combo_products = self.env['product.product'].browse(combo_product)
        products = []
        for cat in combo_products.combo_products_ids:
            inner_product = []
            product_dict = {}
            product_dict['category_name'] = cat.category_id.name
            for product in cat.product_id:
                inner_product.append(
                    {'product_id': product.id, 'product_name': product.name, 'count':cat.item_count, 'required':cat.is_required})
            product_dict['product'] = inner_product
            products.append(product_dict)
        
        return products
