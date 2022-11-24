{
    'name': 'BOM Product Wise Usage Report',
    'version': '16.0.1.0.0',
    'author': "Shubin V S",
    'depends': [
        'base', 'mrp'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/bom_usage_report_wizard.xml',
        'views/bom_usage_report_menu.xml',
        'report/bom_usage_pdf_report_template.xml',
        'report/bom_usage_report_action.xml'
    ]
}
