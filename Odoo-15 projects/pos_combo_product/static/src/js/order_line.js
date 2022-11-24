odoo.define('pos_combo_products.combo_product_in_order_line', function(require) {
     "use strict";
     var models = require('point_of_sale.models');
     var _super_orderline = models.Orderline.prototype;
     models.Orderline = models.Orderline.extend({
            initialize:function(attr,options){
                 _super_orderline.initialize.apply(this, arguments);
                 this.combo_products = this.combo_products || []
            }
     })

});