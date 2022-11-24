from odoo import fields, models


class SaleOrderApproval(models.TransientModel):
    _inherit = 'res.config.settings'

    so_approval = fields.Boolean(string="Sale Order Approval",
                                 config_parameter='spotter_sale_order_approval.so_approval')
    minimum_amount = fields.Float(string="Minimum Amount",
                                  config_parameter='spotter_sale_order_approval.minimum_amount')

    # def set_values(self):
    #     super(SaleOrderApproval, self).set_values()
    #     self.env['ir.config_parameter'].set_param(
    #         'spotter_sale_order_approval.so_approval', self.so_approval)
    #     self.env['ir.config_parameter'].set_param(
    #         'spotter_sale_order_approval.minimum_amount', self.minimum_amount)
    #
    # @api.model
    # def get_values(self):
    #     res = super(SaleOrderApproval, self).get_values()
    #     params = self.env['ir.config_parameter'].sudo()
    #     so_approval = params.get_param(
    #         'spotter_sale_order_approval.so_approval')
    #     res['so_approval'] = so_approval
    #     minimum_amount = params.get_param(
    #         'spotter_sale_order_approval.minimum_amount')
    #     res['minimum_amount'] = minimum_amount
    #     return res


class UserChecking(models.Model):
    _inherit = 'hr.employee'

    logg_id = fields.Many2one('sale.order')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('to_approve', 'To Approve'),
                                            ('second_approval',
                                             'Second Approval'),
                                            ('sent',)
                                            ])

    approver_ids = fields.One2many('hr.employee', 'logg_id')
    check = fields.Boolean(compute='_compute_line_weight')

    def action_confirm(self):
        total = self.amount_total
        params = self.env['ir.config_parameter'].sudo()
        so_approval = params.get_param(
            'spotter_sale_order_approval.so_approval')
        params = self.env['ir.config_parameter'].sudo()
        minimum_amount = params.get_param(
            'spotter_sale_order_approval.minimum_amount')

        if so_approval:
            if self.state == 'draft':
                if total > float(minimum_amount):
                    self.state = 'to_approve'
                else:
                    return super(SaleOrder, self).action_confirm()
            elif self.state == 'sent':
                return super(SaleOrder, self).action_confirm()
        else:
            return super(SaleOrder, self).action_confirm()

    def action_approve(self):
        self.state = 'second_approval'
        record = (
            self.env['sale.order'].browse([self._context.get('active_id')]))
        logged_user_id = self.env.user.id
        record.write({
            'approver_ids': [(0, 0, {
                'name': logged_user_id
            })]
        })

    def _compute_line_weight(self):
        logged_user_id = self.env.user.id
        first_approver_id = self.approver_ids.name
        if int(first_approver_id) == logged_user_id:
            self.check = True
        else:
            self.check = False

    def action_validate(self):
        self.state = 'sent'
        res = super(SaleOrder, self).action_quotation_send()
        return res

    def action_cancel(self):
        self.state = 'cancel'
