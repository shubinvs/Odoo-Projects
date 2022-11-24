from odoo import http
from odoo.http import request


class OnlineWarrantyRequest(http.Controller):

    @http.route(['/warranty_request'], type='http', auth="public",
                website=True)
    def online_warranty_request(self, **post):
        invoice_id = request.env['account.move'].search(
                                    [('state', '=', 'posted'),
                                     ('move_type', '=', 'out_invoice')])
        vals = {
            'invoice_id': invoice_id
        }
        return request.render(
            "product_warranty.tmp_warranty_request_form", vals)

    @http.route(['/warranty_request/submit'], type='http', auth="public",
                website=True)
    def online_warranty_request_submit(self, **post):
        product_warranty = request.env['warranty.request'].sudo().create({
            'invoice_id': post.get('invoice'),
            'customer_id': post.get('name'),
            'product_id': post.get('product'),
            'lot_id': post.get('lot')
        })
        vals = {
            'warranty': product_warranty
        }
        return request.render(
            "product_warranty.tmp_warranty_request_form_success", vals)

    @http.route("/get_products", type="json", auth="public", website=True)
    def warranty_products(self, invoice, **post):
        if invoice:
            invoice_id = request.env['account.move'].sudo().browse(int(invoice))
            customer = invoice_id.partner_id
            customer_list = []
            for rec in customer:
                customer_list.append([rec.id, rec.name])
            product_ids = invoice_id.invoice_line_ids.product_id.ids
            product = request.env['product.product'].sudo().browse(product_ids)
            product_list = []
            for rec in product:
                if rec.has_warranty:
                    product_list.append([rec.id, rec.name])
            vals = {
                    'name': customer_list,
                    'product': product_list
                }
            return vals

    @http.route("/get_lot", type="json", auth="public", website=True)
    def warranty_products_lot(self, product, **post):
        if product:
            lot = request.env['stock.production.lot'].search(
                [('product_id', '=', int(product))])
            lot_list = []
            for rec in lot:
                lot_list.append([rec.id, rec.name])
            vals = {
                'lot': lot_list
            }
            return vals
