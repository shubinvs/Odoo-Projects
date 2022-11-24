import json
import io
import xlsxwriter
from odoo import fields, models
from odoo.tools import date_utils


class WarrantyRequestReportWizard(models.TransientModel):
    _name = 'warranty.report.wizard'
    _description = 'warranty request report wizard'

    product_ids = fields.Many2many('product.template',
                                   domain="[('has_warranty', '=', True)]",
                                   required=True)
    customer_id = fields.Many2one('res.partner')
    start_date = fields.Date()
    end_date = fields.Date()
    today_date = fields.Date.today()

    def action_print_pdf(self):

        query = """select a.sequence_no, b.name as customer_name, c.name as product_name, a.request_date from warranty_request a join res_partner b on a.customer_id=b.id
join product_product d  on d.id = a.product_id join product_template c on c.id = d.product_tmpl_id 
"""
        if self.start_date:
            new_query = """where a.request_date >= '{start_date}'""".format(
                start_date=self.start_date)
            query += new_query

        if self.end_date:
            new_query = """and a.request_date <= '{end_date}'""".format(
                end_date=self.end_date)
            query += new_query

        if self.customer_id:
            new_query = """ and b.name = '{customer_id}'""".format(
                customer_id=self.customer_id.name)
            query += new_query

        product_names = ['']
        for rec in self.product_ids:
            product_names.append(rec.name)
        products = tuple(product_names)
        print(products)
        new_query = """ and c.name in {product_ids} """.format(
            product_ids=products)
        query += new_query

        self.env.cr.execute(query)
        record = self.env.cr.dictfetchall()
        data = {
            'response': record,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'today_date': self.today_date

        }
        return self.env.ref(
            'product_warranty.warranty_request_report_action').report_action(
            None, data=data)

    def action_print_xlsx(self):
        query = """select a.sequence_no, b.name as customer_name, c.name as product_name, a.request_date from warranty_request a join res_partner b on a.customer_id=b.id
        join product_product d  on d.id = a.product_id join product_template c on c.id = d.product_tmpl_id 
        """
        if self.start_date:
            new_query = """where a.request_date >= '{start_date}'""".format(
                start_date=self.start_date)
            query += new_query

        if self.end_date:
            new_query = """and a.request_date <= '{end_date}'""".format(
                end_date=self.end_date)
            query += new_query

        if self.customer_id:
            new_query = """ and b.name = '{customer_id}'""".format(
                customer_id=self.customer_id.name)
            query += new_query

        product_names = ['']
        for rec in self.product_ids:
            product_names.append(rec.name)
        products = tuple(product_names)
        print(products)
        new_query = """ and c.name in {product_ids} """.format(
            product_ids=products)
        query += new_query

        self.env.cr.execute(query)
        record = self.env.cr.dictfetchall()
        print(record)

        data = {
            'response': record,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'today_date': self.today_date

        }
        return {'type': 'ir.actions.report',
                'report_type': 'xlsx',
                'data': {'model': 'warranty.report.wizard',
                         'output_format': 'xlsx',
                         'options': json.dumps(data,
                                               default=date_utils.json_default),
                         'report_name': 'warranty request xlsx report', }

                }

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format({'font_size': '12px', 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px','align': 'center'})
        sheet.set_column('D:D', 20)
        # sheet.set_column(15, 10, 50)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:F', 20)
        sheet.set_column('G:G', 20)
        sheet.merge_range('C2:G3', 'PRODUCT WARRANTY', head)
        sheet.write('C5', 'Date:', cell_format)
        sheet.write('D5', data['today_date'], txt)
        sheet.write('C7', 'From:', cell_format)
        sheet.write('D7', data['start_date'], txt)
        sheet.write('E7', 'To:', cell_format)
        sheet.write('F7', data['end_date'], txt)
        sheet.write('C9', 'SL NO', cell_format)
        sheet.write('D9', 'SEQUENCE NO', cell_format)
        sheet.write('E9', 'CUSTOMER', cell_format)
        sheet.write('F9', 'PRODUCT', cell_format)
        sheet.write('G9', 'REQUEST DATE', cell_format)
        sl_no = 1
        row = 9
        column = 2
        for i in data['response']:
            sheet.write(row, column, sl_no, txt)
            sheet.write(row, column+1, i['sequence_no'], txt)
            sheet.write(row, column+2, i['customer_name'], txt)
            sheet.write(row, column+3, i['product_name'], txt)
            sheet.write(row, column+4, i['request_date'], txt)
            sl_no += 1
            row += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
