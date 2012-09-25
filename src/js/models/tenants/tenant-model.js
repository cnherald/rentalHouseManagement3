define(
['jquery', 'lodash', 'backbone'],

function($, _, Backbone) {

    var Tenant = Backbone.Model.extend({
        urlRoot: "tenants/",
        defaults: {
            "id": null,
            "firstName": "",
            "surname": "",
            "gender": "",
            "age": " ",
            "phoneNumber": "",
            "email": "",
			"registerDate": ""
        }
    });

    return Tenant;
});