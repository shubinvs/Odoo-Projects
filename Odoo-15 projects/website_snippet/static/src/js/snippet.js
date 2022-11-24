odoo.define('website_snippet.dynamic', function (require) {
        "use strict";
    var PublicWidget = require('web.public.widget');
    var ajax = require('web.ajax');
    var Dynamic = PublicWidget.Widget.extend({
       selector: '.js_dynamic_snippet',
       start: function(){
           var self = this;
           ajax.jsonRpc('/online_snippets','call',{}).then(function(res){
               if(res){
                   self.$target.empty().append(res)
                   }
               });
           },
       });
   PublicWidget.registry.js_dynamic_snippet = Dynamic;
    return Dynamic;
});
