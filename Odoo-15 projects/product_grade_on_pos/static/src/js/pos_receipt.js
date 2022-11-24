odoo.define('product_grade_on_pos.receipt', function (require) {
    'use strict';
    const models = require('point_of_sale.models');
    models.load_fields('product.product', 'product_grade');

    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        export_for_printing: function() {
            var line = _super_orderline.export_for_printing.apply(this,arguments);
            line.product_grade = this.get_product().product_grade;
            return line;
        }
    });
});