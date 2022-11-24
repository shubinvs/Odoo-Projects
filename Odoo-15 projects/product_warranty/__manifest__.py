{
    'name': 'Warranty',
    'application': True,
    'sequence': 1,
    'version': '15.0.1.0.0',
    'author': "Shubin V S",
    'depends': ['base', 'account', 'stock', 'sale_management', 'website',
                'mail'],
    'data': [
        'security/security_access.xml',
        'security/ir.model.access.csv',
        'views/warranty_request.xml',
        'views/warranty_request_front_end.xml',
        'report/warranty_request_report_action.xml',
        'report/warranty_request_pdf_report.xml',
        'data/ir_sequence_data.xml',
        'wizard/warranty_request_report_wizard.xml',
        'views/menu.xml',
        'views/website_form_template.xml',
        ''
        'views/website_form_submit_template.xml'

    ],
    'assets': {'web.assets_backend': [
        'product_warranty/static/src/js/action_warranty_request.js']},

    'assets': {'web.assets_frontend': [
        'product_warranty/static/src/js/website_warranty_request.js']}

}
