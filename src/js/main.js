require([
    'jquery',
    'lodash',
    'backbone',
    'views/header',
    'views/start',
    'views/tenant-details',
    'views/tenant-list',
    'utils/tpl',
    'models/tenants/tenant-model',
    'models/tenants/tenant-collection'
],

function($, _, Backbone, HeaderView, StartView, TenantView, TenantListView, tpl, Tenant, TenantCollection) {

    Backbone.View.prototype.close = function() {
        console.log('Closing view ' + this);
        if (this.beforeClose) {
            this.beforeClose();
        }
        this.remove();
        this.unbind();
    };

    var AppRouter = Backbone.Router.extend({

        initialize: function() {
            $('#header').html(new HeaderView().render());
        },

        routes: {
            "": "list",
            "tenants/new": "newTenant",
            "tenants/:id": "tenantDetails"
        },

        list: function() {
            this.before(function() {
                this.showView('#content', new StartView());
            });
        },

        tenantDetails: function(id) {
            alert("test------id= " + id);
            this.before(function() {
                var tenant = this.tenantList.get(id);
                this.showView('#content', new TenantView({
                    model: tenant
                }));
            });
        },

        newTenant: function() {
            this.before(function() {
                this.showView('#content', new TenantView({
                    model: new Tenant()
                }));
            });
        },

        showView: function(selector, view) {
            if (this.currentView) this.currentView.close();

            $(selector).html(view.render());
            this.currentView = view;

            return view;
        },

        before: function(callback) {
            if (this.tenantList) {
                if (callback) callback.call(this);
            } else {
                this.tenantList = new TenantCollection();
                var self = this;
                this.tenantList.fetch({
                    success: function() {
                        var tenantlist = new TenantListView({
                            model: self.tenantList
                        }).render();
                        $('#sidebar').html(tenantlist);
                        if (callback) callback.call(self);
                    }
                });
            }
        }

    });

    tpl.loadTemplates(['header', 'tenant-details', 'tenant-list-item', 'start'], function() {
        window.app = new AppRouter();
        Backbone.history.start();
    });

}); // End require
