define(
['jquery', 'lodash', 'backbone', 'utils/tpl'],

function($, _, Backbone, tpl) {

    var HeaderView = Backbone.View.extend({

        initialize: function() {
            this.template = _.template(tpl.get('header'));
        },

        render: function(eventName) {
            this.$el.html(this.template());
            return this.el;
        },

        events: {
            "click .tenants": "tenantListings",
            "click .rooms": "roomListings"
            //"click .new": "newTenant"
        },
        tenantListings:function(event) {
            app.navigate("tenants/listings", true);
            return false;
        },

        roomListings:function(event) {
            app.navigate("rooms/listings", true);
            return false;
        }
        // newTenant: function(event) {
        //     app.navigate("tenants/new", true);
        //     return false;
        // }

    });

    return HeaderView;

});