require([
    'jquery',
    'lodash',
    'backbone',
    'views/header',
    'views/start',
    'views/tenant-details',
    'views/room-details',
    'views/tenant-list',
    'views/room-list',
    'utils/tpl',
    'models/tenants/tenant-model',
    'models/rooms/room-model',
    'models/tenants/tenant-collection',
    'models/rooms/room-collection'
],

function($, _, Backbone, HeaderView, StartView, TenantView, TenantListView, RoomView, RoomListView, tpl, Tenant, TenantCollection,Room, RoomCollection) {

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
            "tenants/listings": "tenantListings",
            "rooms/listings": "roomsListings",
            "tenant/new": "newTenant",
            "room/new": "newRoom",
            "tenants/:id": "tenantDetails",
            "rooms/:id": "roomDetails"
        },

        list: function() {
             this.showView('#content', new StartView());
            // this.before(function() {
            //     this.showView('#content', new StartView());
            // });
        },

        tenantListings: function() {
            alert("tenant listings !!! " );
            this.tenantBefore(function() {
                var tenant = this.tenantList.get(id);
                this.showView('#content', new TenantView({
                    model: tenant
                }));
            });
        },

        roomsListings: function() {
            alert("room listings !!! " );
            this.before(function() {
                var tenant = this.tenantList.get(id);
                this.showView('#content', new TenantView({
                    model: tenant
                }));
            });
        },


        tenantDetails: function(id) {
            alert("test------id= " + id);
            this.tenantBefore(function() {
                var tenant = this.tenantList.get(id);
                this.showView('#content', new TenantView({
                    model: tenant
                }));
            });
        },

        roomDetails: function(id) {
            alert("test------id= " + id);
            this.roomBefore(function() {
                var room = this.roomList.get(id);
                this.showView('#content', new RoomView({
                    model: room
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

        newRoom: function() {
            this.before(function() {
                this.showView('#content', new RoomView({
                    model: new Room()
                }));
            });
        },

        showView: function(selector, view) {
            if (this.currentView) this.currentView.close();

            $(selector).html(view.render());
            this.currentView = view;

            return view;
        },

        tenantBefore: function(callback) {
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
        },

        roomBefore: function(callback) {
            if (this.roomList) {
                if (callback) callback.call(this);
            } else {
                this.roomList = new RoomCollection();
                var self = this;
                this.roomList.fetch({
                    success: function() {
                        var roomlist = new RoomListView({
                            model: self.roomList
                        }).render();
                        $('#sidebar').html(roomlist);
                        if (callback) callback.call(self);
                    }
                });
            }
        }

    });

    tpl.loadTemplates(['header', 'tenant-details', 'tenant-list-item', 'room-details', 'room-list-item','start'], function() {
        window.app = new AppRouter();
        Backbone.history.start();
    });

}); // End require
