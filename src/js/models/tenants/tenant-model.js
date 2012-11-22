define(
['jquery', 'lodash', 'backbone'],

function($, _, Backbone) {

    var Tenant = Backbone.Model.extend({
        urlRoot: "tenants/",
		//idAttribute: "_id",
        defaults: {
            "id": null,
            "firstName": "",
            "surname": "",
            "gender": "",
            "age": " ",
            "phoneNumber": "",
            "email": "",
			"registerDate": "",
			"picture": ""
			
        }
    });

    return Tenant;
});