from odoo import fields, models, api


class ProductWarranty(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = "warranty.request"
    _description = "Warranty Request"
    _rec_name = 'sequence_no'
    _order = 'sequence_no desc'

    sequence_no = fields.Char(required=True, readonly=True, default='New')
    invoice_id = fields.Many2one('account.move', required=True,
                                 domain="[('state','=','posted'),"
                                        "('move_type','=','out_invoice')]")
    product_id = fields.Many2one('product.product')
    lot_id = fields.Many2one('stock.production.lot')
    request_date = fields.Date(default=fields.Date.today())
    customer_id = fields.Many2one('res.partner')
    purchase_date = fields.Date(string='Purchase Date')
    warranty_expiry_date = fields.Date(string='Warranty Expiry Date')
    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('to_approve', 'To Approve'),
                                        ('approved', 'Approved'),
                                        ('product_received',
                                         'Product Received'),
                                        ('return_product', 'Return Product'),
                                        ('cancel', 'Cancel'),
                                        ('done', 'Done')],
                             string='Status', required=True,
                             readonly=True, copy=False,
                             tracking=True, default='draft')

    def get_warranty_request(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Warranty',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('origin', '=', self.sequence_no)],
            'context': "{'create': False}"
        }

    def button_to_approve(self):
        self.write({'state': "to_approve"})

    def button_approved(self):
        if self.product_id.warranty_type == 'service_warranty' or \
                self.product_id.warranty_type == 'replace_warranty':
            self.write({'state': "approved"})
            picking_type = self.env.ref('stock.picking_type_in')
            cus_location = self.env.ref('stock.stock_location_customers')
            warranty_location = self.env.ref(
                'product_warranty.location_warranty_location')
            self.env['stock.picking'].create({
                'picking_type_id': picking_type.id,
                'location_id': cus_location.id,
                'location_dest_id': warranty_location.id,
                'partner_id': self.customer_id.id,
                'origin': self.sequence_no,

                'move_ids_without_package': [(0, 0, {
                    'name': self.product_id.id,
                    'product_id': self.product_id.id,
                    'product_uom': self.product_id.uom_id.id,
                    'location_id': cus_location.id,
                    'location_dest_id': warranty_location.id

                })]
            })

    def button_draft(self):
        self.write({'state': "draft"})

    def button_cancel(self):
        self.write({'state': "cancel"})

    def button_return_button(self):
        self.write({'state': "return_product"})
        picking_type = self.env.ref('stock.picking_type_out')
        cus_location = self.env.ref('stock.stock_location_customers')
        warranty_location = self.env.ref(
            'product_warranty.location_warranty_location')
        self.env['stock.picking'].create({
            'picking_type_id': picking_type.id,
            'location_id': warranty_location.id,
            'location_dest_id': cus_location.id,
            'partner_id': self.customer_id.id,
            'origin': self.sequence_no,

            'move_ids_without_package': [(0, 0, {
                'name': self.product_id.id,
                'product_id': self.product_id.id,
                'product_uom': self.product_id.uom_id.id,
                'location_id': warranty_location.id,
                'location_dest_id': cus_location.id

            })]
        })

    @api.onchange('invoice_id')
    def _onchange_invoice_id(self):
        if self.invoice_id:
            self.purchase_date = self.invoice_id.invoice_date
            self.customer_id = self.invoice_id.partner_id
            product_list = self.invoice_id.invoice_line_ids.product_id.ids
            return {'domain': {'product_id': [('id', '=', product_list),
                                              ('has_warranty', '=', True)]}}

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            return {'domain': {'lot_id': [('product_id', '=',
                                           self.product_id.id)]}}

    @api.onchange('product_id', 'purchase_date')
    def _onchange_warranty(self):
        if self.product_id:
            self.warranty_expiry_date = fields.Date.add(
                self.purchase_date,
                days=self.product_id.warranty_period)

    @api.model
    def create(self, vals):
        if vals.get('sequence_no', 'New') == 'New':
            vals['sequence_no'] = self.env['ir.sequence']. \
                                      next_by_code('sequence.number') or 'New'
        result = super(ProductWarranty, self).create(vals)
        return result


class Product(models.Model):
    _inherit = 'product.template'

    has_warranty = fields.Boolean()
    warranty_period = fields.Integer('Warranty Period')
    warranty_type = fields.Selection(string='Warranty Type',
                                     selection=[
                                         ('service_warranty',
                                          'Service Warranty'),
                                         ('replace_warranty',
                                          'Replace Warranty')
                                     ])


class StateChange(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StateChange, self).button_validate()
        result = self.env['warranty.request'].search(
            [('sequence_no', '=', self.origin)])
        print(result)
        if result.state == 'approved':
            result.state = 'product_received'
        elif result.state == 'return_product':
            result.state = 'done'
        return res


class Invoice(models.Model):
    _inherit = 'account.move'

    warranty_info_ids = fields.One2many('warranty.request',
                                        'invoice_id')
