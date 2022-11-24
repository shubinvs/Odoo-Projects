odoo.define('combo_product_on_pos.combo_product', function(require){
    "use strict";

        var models = require('point_of_sale.models');
        var rpc = require('web.rpc');

        const ProductScreen = require('point_of_sale.ProductScreen');
        const Registries = require('point_of_sale.Registries');

        var core = require('web.core');
        var _t = core._t;


        const ComboProducts = (ProductScreen) =>
            class extends ProductScreen {
                async _clickProduct(event){
                    console.log('start.........')
                    var self = this
                    const product = event.detail;
                    const options = await this._getAddProductOptions(product);
                    await super._clickProduct(event);
                    var display_name = product['display_name']
                    var combo_product = product['combo_ids']
                    console.log('**************',combo_product)
                    if (combo_product[0]){
                        var results;
                        await rpc.query({
                            model : 'product.product',
                            method : 'get_product_details',
                            args : [product.id]
                        }).then(function(result){
                            results = result
                            console.log('!!!!!!!!!!!!!!!!!!!!!!111',results)
                        });
                        await this.showPopup("ComboProductsPopup",{
                            title: _t("Combo Products"),
                            DisplayName: display_name,
                            Result: results,
                            confirmText: _t("Confirm"),
                            exitText: _t('Cancel')
                        });
                    }
                }
            };

        Registries.Component.extend(ProductScreen, ComboProducts)
        return ProductScreen;
});