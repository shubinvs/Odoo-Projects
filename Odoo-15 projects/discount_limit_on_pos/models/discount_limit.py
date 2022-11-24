from odoo import fields, models


class DiscountLimit(models.Model):
    _inherit = 'pos.config'

    discount = fields.Boolean(string="Discounts")
    pos_category = fields.Many2one('pos.category', string="Pos Category")
    discount_limit = fields.Float(string="Discount Limit")
