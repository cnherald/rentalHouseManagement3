define(
['jquery', 'lodash', 'backbone'],

function($, _, Backbone) {

    var Tenant = Backbone.Model.extend({
        urlRoot: "tenants/",
        //urlRoot: "tenant",
		//idAttribute: "_id",

/*        methodToURL: {
            'read': '/user/get',
            'create': '/user/create',
            'update': '/tenants/update',
            'delete': '/user/remove'
        },

        sync: function(method, model, options) {
            options = options || {};
            options.url = model.methodToURL[method.toLowerCase()];

            Backbone.sync(method, model, options);
        },*/





        sync: function(method, model, options){
              if(method =='GET'){
                options.url = model.urlRoot; 
              }else if(method == 'create'){
                options.url = model.urlRoot; 
              } else if (method == "delete"){               
                options.url = model.urlRoot + 'delete?tenantId=' + model.id;       

              } else {
                 //options.url = model.urlRoot + 'update?tenantId='+model.id;
                 options.url = model.urlRoot + 'update'; 
              }
              return Backbone.sync(method, model, options);
        },

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