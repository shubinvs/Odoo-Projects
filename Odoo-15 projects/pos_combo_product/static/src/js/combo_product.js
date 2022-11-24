/** @odoo-module **/
import AbstractAwaitablePopup from 'point_of_sale.AbstractAwaitablePopup';
import Registries from 'point_of_sale.Registries';
import PosComponent from 'point_of_sale.PosComponent';
import ControlButtonsMixin from 'point_of_sale.ControlButtonsMixin';
import NumberBuffer from 'point_of_sale.NumberBuffer';
import { useListener } from 'web.custom_hooks';
import { onChangeOrder, useBarcodeReader } from 'point_of_sale.custom_hooks';
const { useState } = owl.hooks;
class ComboProductsPopup extends AbstractAwaitablePopup {
    constructor() {
        super(...arguments);
        this.selectedProducts = [];
        this.product_id = [];
        useListener('click-product', this._clickProduct);
    }
    confirm() {
        var self = this;
        console.log("product display", this.selectedProducts);
        console.log("current orderlines",this.env.pos.get_order().get_orderlines())
        this.env.pos.get_order().get_selected_orderline().combo_products = this.selectedProducts;
        console.log("current orderlines 123",this.env.pos.get_order().get_selected_orderline())
        var requiredProducts = this.props.Result;
        requiredProducts.forEach(function(item){
           item.product.forEach(function(n){
             if (n.required == true){
              self.selectedProducts.push({
                 'product_id': n['product_id'],
                 'product_name':n['product_name'],
                 'quantity':n['count'],
              });
             };
           });
        });
        this.trigger('close-popup');
    }
    cancel() {
        console.log("popup cancel");
        this.trigger('close-popup');
    }
    _clickProduct(product) {
        console.log("GET ORDER",this.env.pos.get_order().orderlines)
        var self = this;
        var dict = {}
        var checkProductId = this.props.Result
        checkProductId.forEach(function(item){
          item.product.forEach(function(m){
           if (m.required == true){
           self.product_id.push(m['product_id'])
           };
          })
        })

        if (!$("#select_product_" + product['product_id']).hasClass('hidden')) {
            $(".check").addClass('hidden');
            console.log(self.product_id, "Product #######")
            if (!self.product_id.includes(product['product_id'])){
            this.selectedProducts.push({
                'product_id': product['product_id'],
                'product_name':product['product_name'],
                'quantity': product['count'],
            })
            $("#select_product_" + product['product_id']).addClass('fa');
            $("#select_product_" + product['product_id']).addClass('fa-check-circle');
           }
        } else {
            delete this.selectedProducts[product['product_id']]
            $(".check").removeClass("hidden");
            $("#select_product_" + product['product_id']).removeClass('fa');
            $("#select_product_" + product['product_id']).removeClass('fa-check-circle');
        }
    }

}
//Create products popup
ComboProductsPopup.template = 'ComboProductsPopup';
ComboProductsPopup.defaultProps = {
    confirmText: 'Ok',
    cancelText: 'Cancel',
    title: 'Combo Products',
    body: '',
};
Registries.Component.add(ComboProductsPopup);
export default ComboProductsPopup;
