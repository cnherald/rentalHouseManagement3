define(
['jquery', 'lodash', 'backbone'],

function($, _, Backbone) {

    var Tenant = Backbone.Model.extend({
        urlRoot: "tenants/",
        defaults: {
            "id": null,
            "firstName": "",
            "secondName": "",
            "Gender": "",
            "Age": " ",
            "year": "",
            "Mobile": "",
            "email": ""
        }
    });

    return Tenant;
});