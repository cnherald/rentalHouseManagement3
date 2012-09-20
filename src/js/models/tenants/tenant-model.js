define(
['jquery', 'lodash', 'backbone'],

function($, _, Backbone) {

    var Tenant = Backbone.Model.extend({
        urlRoot: "tenants/",
        defaults: {
            "id": null,
            "FirstName": "",
            "Surname": "",
            "Gender": "",
            "Age": " ",
            "PhoneNumber": "",
            "Email": ""
        }
    });

    return Tenant;
});