from odoo import fields, models, api


class ContactTolerance(models.Model):
    _inherit = 'res.partner'

    tolerance = fields.Float(string="Tolerance")


class SaleOrderTolerance(models.Model):
    _inherit = "sale.order"

    tolerance = fields.Float(string="Tolerance")

    @api.onchange('partner_id')
    def _onchange_partner(self):
        if self.partner_id:
            self.tolerance = self.partner_id.tolerance


class ToleranceChecking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        for rec in self.move_ids_without_package:
            demand = rec.product_uom_qty
            print(demand)
            done = rec.quantity_done
            print(done)
            res_tol = rec.partner_id.tolerance
            print(res_tol)
            differ = demand * res_tol
            print(differ)
            min_tol = demand - differ
            print('min tolerance range', min_tol)
            max_tol = demand + differ
            print('max tolerance range', max_tol)

            if min_tol <= done <= max_tol:
                res = super(ToleranceChecking, self).button_validate()
                return res

            else:

                return {
                    'name': 'Warning!!!!!!',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'tolerance.wizard',
                    'target': 'new'
                }
