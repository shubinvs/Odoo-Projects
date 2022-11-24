{
    'name': 'POS Combo Product',
    'version': '15.0.1.0.0',
    'author': "Shubin V S",
    'depends': [
        'base', 'point_of_sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_combo_product.xml'
    ],
    'assets': {
        'point_of_sale.assets': [
            'combo_product_on_pos/static/src/js/combo_product.js',
            'combo_product_on_pos/static/src/js/combo_product_popup.js',
            'combo_product_on_pos/static/src/js/combo_product_receipt.js',
            'combo_product_on_pos/static/src/xml/combo_product_label.xml',
            'combo_product_on_pos/static/src/xml/combo_product_popup.xml',
            'combo_product_on_pos/static/src/xml/combo_product_orderline.xml',
            'combo_product_on_pos/static/src/xml/combo_product_receipt.xml'
        ]
    },
}
