{
    'name': 'SALES ORDER',
    'version': '15.0.1.0.0',
    'author': "Shubin V S",
    'depends': [
        'base', 'sale_management'
    ],
    'data': [
        'security/ir.model.access.csv',
        'report/sales_report_pdf_report_template.xml',
        'report/sales_report_action.xml',
        'views/sales_report.xml',
        'data/scheduled_action.xml',
    ]
}
