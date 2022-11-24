from odoo import fields, models


class Product(models.Model):
    _inherit = 'product.template'

    product_grade = fields.Selection(selection=[('A', 'A'), ('B', 'B'),
                                                ('C', 'C'), ('D', 'D')])
