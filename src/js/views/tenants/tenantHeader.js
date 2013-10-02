define(
['jquery', 'lodash', 'backbone', 'utils/tpl'],

function($, _, Backbone, tpl) {

    var tenantHeaderView = Backbone.View.extend({

        initialize: function() {
            //alert("tenantHeaderView is here!!");
            this.template = _.template(tpl.get('tenantHeader'));
        },

        render: function(eventName) {
            this.$el.html(this.template());
            return this.el;
        },

        events: {
            //"click .tenants": "tenantListings",
            "click .new": "newTenant"
        },
        // tenantListings:function(event) {
        //     app.navigate("tenants/listings", true);
        //     return false;
        // },
        newTenant: function(event) {
            app.navigate("tenant/new", true);
            return false;
        }

    });

    return tenantHeaderView;

});