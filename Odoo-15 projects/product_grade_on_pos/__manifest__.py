{
    'name': "PRODUCT GRADE",
    'sequence': '5',
    'application': True,
    'version': '15.0.1.0.0',
    'author': "Shubin V S",
    'depends': [
        'base', 'point_of_sale'
    ],
    'data': [
        'views/product_grade.xml'
    ],
    'assets': {
        'web.assets_qweb': [
            'product_grade_on_pos/static/src/xml/pos_receipt.xml'
        ],
        'web.assets_backend': [
            'product_grade_on_pos/static/src/js/pos_receipt.js',
        ],
    }
}
