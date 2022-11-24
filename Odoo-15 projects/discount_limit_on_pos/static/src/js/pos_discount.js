odoo.define('discount_limit_on_pos.receipt', function (require) {
    'use strict';

    const models = require('point_of_sale.models');
    models.load_fields('product.product', 'pos_categ_id');

    var { Gui } = require('point_of_sale.Gui');
    const PosComponent = require("point_of_sale.PosComponent");
    const ProductScreen = require("point_of_sale.ProductScreen");
    const Registries = require("point_of_sale.Registries");


    var existing_models = models.PosModel.prototype.models;
    const CustomDiscountLimit = (ProductScreen) =>
    class extends ProductScreen{
        constructor() {
            super(...arguments);
        }
        async _onClickPay() {

            var limit_crossed = false;
            var discount = this.env.pos.config.discount;
            var discount_category = this.env.pos.config.pos_category[1];
            var max_discount_limit = this.env.pos.config.discount_limit;

            var order = this.env.pos.get_order();
            var lines = order.get_orderlines()
            if (discount) {
                var total_discount = 0;
                lines.forEach(function(element) {
                    if (element.product.pos_categ_id[1] == discount_category){
                        var discount_amount = element.price * (element.discount/100);
                        total_discount += discount_amount;
                        if (total_discount > max_discount_limit){
                            limit_crossed = true;
                        }
                    }
                });
                if (limit_crossed){
                    await this.showPopup('ErrorPopup', {
                        title: ('Error PopUp'),
                        body: ('discount Limit is exceeded!!!!!!')
                    });
                }
                else{
                    await super._onClickPay(...arguments);
                }
            }
        }
    }
    Registries.Component.extend(ProductScreen,CustomDiscountLimit);
    return CustomDiscountLimit;
});
