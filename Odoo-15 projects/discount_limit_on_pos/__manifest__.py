{
    'name': 'POS DISCOUNT LIMIT',
    'application': True,
    'sequence': 4,
    'version': '15.0.1.0.0',
    'author': "Shubin V S",
    'depends': ['base', 'point_of_sale'],
    'data': [
        'views/discount_limit.xml'
    ],
    'assets': {
        'point_of_sale.assets': [
            'discount_limit_on_pos/static/src/js/pos_discount.js'
        ]
    }
}
