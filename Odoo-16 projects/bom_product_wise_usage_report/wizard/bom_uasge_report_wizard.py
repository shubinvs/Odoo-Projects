from odoo import fields, models


class BomUsageReport(models.TransientModel):
    _name = 'bom.usage.report.wizard'
    _description = 'bom usage report wizard'

    from_date = fields.Date(string="From Date ")
    to_date = fields.Date(string="To Date ")
    product_id = fields.Many2one('product.product')
    reduce_unbuild_order = fields.Boolean(string='Reduce unbuild orders')

    def action_print_pdf(self):
        query = """ select product_template_1.name as component_product,product_template_1.default_code as component_product_code, product_template_2.name as final_product,product_template_2.default_code as final_product_code,mrp_bom.product_qty as quantity,uom_uom.name as uom
                from product_template  product_template_1
                join mrp_bom_line on product_template_1.id = mrp_bom_line.product_tmpl_id
                join mrp_bom on mrp_bom_line.bom_id = mrp_bom.id
                join product_template product_template_2 on mrp_bom.product_tmpl_id = product_template_2.id
                join uom_uom  on uom_uom.id = mrp_bom.product_uom_id
                 """

        if self.from_date:
            new_query = """where mrp_bom.create_date >= '{from_date}'""".format(
                from_date=self.from_date)
            query += new_query

        if self.to_date:
            new_query = """and mrp_bom.create_date <= '{to_date}'""".format(
                to_date=self.to_date)
            query += new_query

        if self.product_id:
            new_query = """and product_template_1.id = '{product_id}'""".format(
                product_id=self.product_id.product_tmpl_id.id)
            query += new_query

        unbuild_list_name = []
        unbuild_list = []
        if self.reduce_unbuild_order:
            unbuild = self.env['mrp.unbuild'].search([])
            for rec in unbuild:
                unbuild_list_name.append('['+rec.product_id.default_code+']'+rec.product_id.name)
                unbuild_list.append(
                    {
                        'unbuild_product_name': '['+rec.product_id.default_code+']'+rec.product_id.name,
                        'unbuild_product_qty': rec.product_qty
                    }
                )

        self.env.cr.execute(query)
        record = self.env.cr.dictfetchall()

        component = []
        inner_component = []
        for rec in record:
            component.append(
                '[' + rec['component_product_code'] + ']' +
                rec['component_product'][
                    'en_US'])

        non_component = [*set(component)]
        for component_product in non_component:
            for rec in record:
                if '[' + rec['component_product_code'] + ']' + \
                        rec['component_product'][
                            'en_US'] == component_product:
                    inner_component.append(
                        {
                            'component_product': component_product,
                            'final_product': '[' + rec[
                                'final_product_code'] + ']' +
                                             rec['final_product']['en_US'],
                            'qty': rec['quantity'],
                            'uom': rec['uom']['en_US']
                        })

        if self.reduce_unbuild_order:
            data = {
                'response': record,
                'unbuild_list_name': unbuild_list_name,
                'unbuild_list': unbuild_list,
                'component': non_component,
                'final': inner_component,
                'from_date': self.from_date,
                'to_date': self.to_date
            }

            return self.env.ref(
                'bom_product_wise_usage_report.bom_usage_pdf_report_action').report_action(
                None, data=data)
        else:
            data = {
                'response': record,
                'component': non_component,
                'final': inner_component,
                'from_date': self.from_date,
                'to_date': self.to_date
            }

            return self.env.ref(
                'bom_product_wise_usage_report.bom_usage_pdf_report_action').report_action(
                None, data=data)
