define(
['jquery', 'lodash', 'backbone', 'models/tenants/tenant-model'],

function($, _, Backbone, Tenant) {

	var TenantCollection = Backbone.Collection.extend({
		model: Tenant,
		url: "tenants/"
	});

	return TenantCollection;
});