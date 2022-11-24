/** @odoo-module **/
    const PosComponent = require('point_of_sale.PosComponent');
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const ControlButtonsMixin = require('point_of_sale.ControlButtonsMixin');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const { useListener } = require("@web/core/utils/hooks");
    const { onChangeOrder } = require('point_of_sale.custom_hooks');
    const { useBarcodeReader } = require('point_of_sale.custom_hooks');
    const { useState } = owl;
    const ProductItem = require('point_of_sale.ProductItem');


   class ComboProductsPopup extends AbstractAwaitablePopup {
         setup(){
                super.setup(...arguments);
                this.selectedProducts = [];
                this.product_id = [];
                useListener('click', this._clickProduct);
        }

        cancel() {
            console.log("popup cancel");
            this.env.posbus.trigger('close-popup', {
                    popupId: this.props.id
                });
        }

        _clickProduct(p){
           try{
                var prod_id = p.path[1].children[0].children[0].id
                var qty = p.path[1].children[2].id
                var prod_name = p.path[1].children[1].alt
                console.log("GET ORDER",this.env.pos.get_order().orderlines)
                var self = this;
                var checkProductId = this.props.Result
                checkProductId.forEach(function(item){
                    item.product.forEach(function(m){
                        if (m.required == true){
                            self.product_id.push(m.product_id)
                        };
                    })
                })
                console.log('||||||||',self.product_id )
                 if (!$("#" + prod_id).hasClass('hidden')) {
                        $(".check").addClass('hidden');
                        console.log('1',self.product_id,typeof(self.product_id))
                        console.log('2',prod_id,typeof(prod_id))
                        if (!self.product_id.includes(parseInt(prod_id))){
                            console.log('Trueeeeee')
                            this.selectedProducts.push({
                            'product_id': parseInt(prod_id),
                            'product_name':prod_name,
                            'quantity': parseInt(qty)
                            });
                            console.log('_______________',this.selectedProducts)
                            $("#" + prod_id).addClass('fa');
                            $("#" + prod_id).addClass('fa-check-circle');
                       }
                    } else {
                        this.selectedProducts.pop(prod_id)
                        console.log('_______________',this.selectedProducts)
                        $(".check").removeClass("hidden");
                        $("#" + prod_id).removeClass('fa');
                        $("#" + prod_id).removeClass('fa-check-circle');
                    }
                    function multiply(qty,num){

                    }
           }
           catch{}
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
                     'quantity': n['count']
                  });
                 };
               });
            });
            this.env.posbus.trigger('close-popup', {
                    popupId: this.props.id
                });
        }


       }

    //Create products popup
   ComboProductsPopup.template = 'ComboProductsPopup';
   ComboProductsPopup.defaultProps = {};

   Registries.Component.add(ComboProductsPopup);
   export default ComboProductsPopup;