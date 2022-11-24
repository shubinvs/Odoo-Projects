from odoo import fields, models, api
from ast import literal_eval
import calendar
import base64
from datetime import datetime


class SalesOrderConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    customer_ids = fields.Many2many('res.partner', string="Customers")
    sales_team_id = fields.Many2one('crm.team', string="Sales Team",
                                    config_parameter='sales_report.sales_team_id')
    based_on = fields.Selection(selection=[('weekly', 'Weekly'),
                                           ('monthly', 'Monthly')],
                                string="Based On",
                                config_parameter='sales_report.based_on',
                                )
    from_date = fields.Datetime(string="Start From",
                                config_parameter='sales_report.from_date')
    to_date = fields.Datetime(string="End To",
                              config_parameter='sales_report.to_date')

    def set_values(self):
        res = super(SalesOrderConfig, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'sales_report.customer_ids', self.customer_ids.ids)
        return res

    @api.model
    def get_values(self):
        res = super(SalesOrderConfig, self).get_values()
        param = self.env['ir.config_parameter'].sudo()
        customers = param.get_param('sales_report.customer_ids')
        res.update(customer_ids=[(6, 0, literal_eval(customers))]
        if customers else False, )
        return res

    @api.onchange('based_on')
    def _onchange_based_on(self):
        schedule_action_id = self.env.ref(
            'sales_report.ir_cron_scheduler_recurring_action')
        if self.based_on == 'weekly':
            schedule_action_id.interval_type = 'weeks'
        elif self.based_on == 'monthly':
            schedule_action_id.interval_type = 'months'
        else:
            schedule_action_id.interval_type = 'days'


class SalesOrderReport(models.Model):
    _name = 'sales.report'

    @api.model
    def sales_order_report(self):
        today_date = fields.Datetime.now()

        param = self.env['ir.config_parameter'].sudo()
        start_date = param.get_param('sales_report.from_date')
        date_time_obj = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')

        param = self.env['ir.config_parameter'].sudo()
        end_date = param.get_param('sales_report.to_date')
        end_date_time_obj = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

        if (today_date > date_time_obj) and (today_date < end_date_time_obj):

            query = """ select sale_order.create_date, sale_order.name as sale_order_name, res_partner.name as customer_name, crm_team.name as sales_team, sale_order.state as status, sale_order.amount_total as total from sale_order 
                                    join res_partner on sale_order.partner_id = res_partner.id join crm_team on sale_order.team_id = crm_team.id  """

            param = self.env['ir.config_parameter'].sudo()
            sales_team = param.get_param('sales_report.sales_team_id')

            if sales_team:
                new_query = """where sale_order.team_id = {sales_team}""".format(
                    sales_team=sales_team)
                query += new_query

            param = self.env['ir.config_parameter'].sudo()
            customers = param.get_param('sales_report.customer_ids')

            result_1 = customers[1:-1]
            altered_string = result_1.split(",")
            int_list = []
            for i in altered_string:
                int_list.append(int(i))
            if len(int_list) == 1:
                new_query = """ and res_partner.id = {customer_ids}""".format(
                    customer_ids=result_1)
                query += new_query
            elif len(int_list) > 1:
                customer_ids = tuple(int_list)

                new_query = """ and res_partner.id in {customer_ids}""".format(
                    customer_ids=customer_ids)
                query += new_query

            self.env.cr.execute(query)
            record = self.env.cr.dictfetchall()

            record_list = []
            weeks = []
            months = []
            for rec in record:
                date = rec['create_date'].day
                month_no = rec['create_date'].month
                month = calendar.month_name[month_no]
                months.append(month)

                if date < 7:
                    rec.update({'week': 'week 1', 'month': month})
                    weeks.append('week 1')
                elif date < 14:
                    rec.update({'week': 'week 2', 'month': month})
                    weeks.append('week 2')
                elif date < 21:
                    rec.update({'week': 'week 3', 'month': month})
                    weeks.append('week 3')
                else:
                    rec.update({'week': 'week 4', 'month': month})
                    weeks.append('week 4')
                record_list.append(rec)

            weeks_order = list(sorted(set(weeks)))

            months_order = list(set(months))

            action_id = self.env.ref(
                'sales_report.ir_cron_scheduler_recurring_action')

            customers_ids = self.env['res.partner'].search(
                [('id', 'in', customer_ids)])

            email_ids = []
            for rec in customers_ids:
                email_ids.append(rec.email)

            data = {
                'response': record_list,
                'months': months_order,
                'weeks': weeks_order,
                'based_on': action_id.interval_type
            }

            pdf = self.env.ref('sales_report.sales_report_action')._render_qweb_pdf(
                self, data=data)

            data_record = base64.b64encode(pdf[0])

            attachment = self.env['ir.attachment'].create({
                'name': 'report.pdf',
                'type': 'binary',
                'datas': data_record,
                'store_fname': data_record,
                'mimetype': 'application/x-pdf',
            })

            for rec in email_ids:
                main_content = {
                    'subject': ('sales report'),
                    'body_html': "SALES REPORT",
                    'email_to': rec,
                    'attachment_ids': attachment

                }

                self.env['mail.mail'].create(main_content).send()
