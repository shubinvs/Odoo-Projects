odoo.define('combo_product_on_pos.combo_receipt.js', function(require){
    "use strict";


    var { Orderline } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');

    const ComboProduct = (Orderline) => class ComboProduct extends Orderline {
    export_for_printing() {
        var line = super.export_for_printing(...arguments);
        line.combo_products = this.combo_products;
        return line;
    }
}
Registries.Model.extend(Orderline, ComboProduct);

});
