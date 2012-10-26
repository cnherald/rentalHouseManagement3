define(
['jquery', 'lodash', 'backbone', 'utils/tpl'],

function($, _, Backbone, tpl) {

    var TenantListView = Backbone.View.extend({

        tagName: 'ul',

        initialize: function() {
            this.model.bind("reset", this.render, this);
            this.model.bind("add", this.appendNewTenant, this);
        },

        render: function(eventName) {
            _.each(this.model.models, function(tenant) {
                this.appendNewTenant(tenant);
            }, this);
            return this.el;
        },

        appendNewTenant: function(tenant) {
            this.$el.append(new TenantListItemView({
                model: tenant
            }).render());
        }
    });

    var TenantListItemView = Backbone.View.extend({

        tagName: "li",
		events:{
			"click #tenantFirstName": "alertMsg"
		},
        initialize: function() {
            this.template = _.template(tpl.get('tenant-list-item'));
            this.model.bind("change", this.render, this);
            this.model.bind("destroy", this.close, this);
        },
		alertMsg: function(){
			alert("test!!!!");
			app.navigate('tenants/' + this.model.id, true); 
			//return false;
		},
        render: function(eventName) {
            this.$el.html(this.template(this.model.toJSON()));
            return this.el;
        }

    });

    return TenantListView;

});