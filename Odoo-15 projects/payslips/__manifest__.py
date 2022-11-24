{
    'name': "PAYSLIPS",
    'application': True,
    'sequence': '3',

    'depends': [
        'base', 'hr', 'hr_payroll_community', 'hr_payslip_monthly_report'
    ],

    'data': [
        'views/payslip_portal.xml',
        'views/payslip_portal_template.xml',
        'views/payslip_print_pdf_action.xml',
        'views/payslip_print_pdf_template.xml'
    ]
}
