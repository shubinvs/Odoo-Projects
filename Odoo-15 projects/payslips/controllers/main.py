from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class WebsiteCustomerPayslipPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        
        values = super(WebsiteCustomerPayslipPortal, self)._prepare_home_portal_values(counters)

        record = request.env['hr.employee'].sudo().search(
            [('user_id', '=', request.env.user.login)])

        payslip_id = request.env['hr.payslip'].sudo().search(
            [('state', '=', 'done'),
             ('employee_id', '=', record.id)])

        payslip_count = len(payslip_id)

        values.update({
            'payslip_count': payslip_count,
        })
        return values


class PortalPayslip(http.Controller):

    @http.route(['/my/payslips'], type='http', auth="public", website=True)
    def portal_payslip(self, **post):

        record = request.env['hr.employee'].sudo().search(
            [('user_id', '=', request.env.user.login)])

        payslip = request.env['hr.payslip'].sudo().search(
                                    [('state', '=', 'done'),
                                     ('employee_id', '=', record.id)])
        
        values = {
            'payslip': payslip
        }
        return request.render("payslips.portal_my_payslip", values)

    @http.route(['/my/<int:id>'], type='http', auth="public", website=True)
    def portal_payslip_page(self, id):

        payslip = request.env['hr.payslip'].sudo().search(
            [('id', '=', id)])
        values = {
            'payslip': payslip
        }


        pdf = request.env.ref('payslips.payslip_report_action').with_context(values)._render_qweb_pdf([payslip.id])[0]
        html_to_pdf = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        return request.make_response(pdf, headers=html_to_pdf)
