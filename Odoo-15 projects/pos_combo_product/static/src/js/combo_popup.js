odoo.define('pos_combo_product.combo_products_in_product_item', function(require) {
    "use strict";

    var models = require('point_of_sale.models');
    var rpc = require('web.rpc')

    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');

    models.load_fields('product.product', 'combo_products_ids')
    models.load_fields('combo.product', 'category_id,product_id,is_required,item_count')

    const ComboProducts = (ProductScreen) =>
        class extends ProductScreen {
            async _clickProduct(event) {
                var self = this;
                const product = event.detail;
                const options = await this._getAddProductOptions(product);
                await super._clickProduct(event);
                var display_name = product['display_name']
                var combo_product = product['combo_products_ids']
                var requiredProducts = [];
                if (combo_product[0]) {
                    var results;
                    await rpc.query({
                        model: 'combo.product',
                        method: 'get_products',
                        args: [product.id]
                    }).then(function(result){
                        results = result
                        console.log("@@@@@@@@@@@",results)
                    });

                    var core = require('web.core');
                    var _t = core._t;
                    await this.showPopup("ComboProductsPopup", {
                        title: _t("Combo Products"),
                        DisplayName: display_name,
                        Result: results,
                        confirmText: _t("Confirm"),
                        exitText: _t('Exit')
                    });
                }
            }
        };
    Registries.Component.extend(ProductScreen, ComboProducts);
    return ProductScreen;
});


