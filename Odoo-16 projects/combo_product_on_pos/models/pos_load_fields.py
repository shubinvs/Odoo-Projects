from odoo import models


class PosLoadFields(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result['search_params']['fields'].append('is_combo')
        result['search_params']['fields'].append('combo_ids')
        print('aaaaaaaaaa', result)
        return result
