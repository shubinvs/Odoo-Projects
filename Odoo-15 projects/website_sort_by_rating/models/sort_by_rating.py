from odoo import fields, models, api


class SortByRating(models.Model):
    _inherit = 'product.template'

    avg_rating = fields.Float(store=True, compute='_compute_rating')

    @api.depends('rating_avg')
    def _compute_rating(self):
        for rec in self:
            rec.avg_rating = rec.rating_avg
