odoo.define('product_warranty.online_warranty', function (require) {
        "use strict";

        var ajax = require('web.ajax');
        $(function(){
            $('#invoice').on('change', function(){
                var invoice = $('select[name=invoice]').val();
                ajax.jsonRpc('/get_products','call',{
                    'invoice': invoice
                }).then(function(response){
                    response['name'].forEach(element => {
                        $('#name').html($('#name').html()+ `<option value=${element[0]}>${element[1]}</option>`)
                    });
                    $('#product').html('<option></option>')
                    response['product'].forEach(element => {
                            $('#product').html($('#product').html()+ `<option value=${element[0]}>${element[1]}</option>`)
                    });
                });
            });
            $('#product').on('change', function(){
                var product = $('select[name=product]').val();
                 ajax.jsonRpc('/get_lot','call',{
                    'product': product
                }).then(function(response){
                    $('#lot').html('<option></option>')
                    response['lot'].forEach(element => {
                            $('#lot').html($('#lot').html()+ `<option value=${element[0]}>${element[1]}</option>`)
                    });
                });
            });
        });
});
