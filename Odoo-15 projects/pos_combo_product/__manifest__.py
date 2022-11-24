{
    'name': 'Pos Combo Product',
    'version': '15.0.1.0.0',
    'description': """
    This module provides features to show combo products in pos.
    """,
    'depends': ['product', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pos_combo_product/static/src/js/combo_product.js',
            'pos_combo_product/static/src/js/combo_popup.js',
            'pos_combo_product/static/src/js/order_line.js',
            'pos_combo_product/static/src/js/combo_product_in_reciept.js',

        ],
        'web.assets_qweb': [
            'pos_combo_product/static/src/xml/combo_product_pos.xml',
            'pos_combo_product/static/src/xml/combo_product_popup.xml',
            'pos_combo_product/static/src/xml/combo_products_in_orderline.xml',
            'pos_combo_product/static/src/xml/combo_products_in_reciept.xml',
        ],
    },
    'license': 'LGPL-3',
    'application': True,
}
