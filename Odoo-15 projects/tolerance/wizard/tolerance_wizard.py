from odoo import models


class ToleranceWizard(models.TransientModel):
    _name = 'tolerance.wizard'
    _description = 'tolerance wizard'

    def action_accept(self):
        record = (self.env['stock.picking'].browse([self._context.get('active_id')]))
        record._action_done()

    def action_dont_accept(self):
        return {'type': 'ir.actions.act_window_close'}
