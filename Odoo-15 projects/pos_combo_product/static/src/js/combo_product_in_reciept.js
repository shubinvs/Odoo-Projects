odoo.define('pos_combo_products.combo_products_receipt.js', function(require){
    "use strict";
    var models = require('point_of_sale.models');
//    models.load_fields('product.product', 'combo_products');
    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        export_for_printing: function(){
            var line = _super_orderline.export_for_printing.apply(this, arguments);
            line.combo_products = this.combo_products;
            return line;
        }
    });
});