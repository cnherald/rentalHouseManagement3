define(
['jquery', 'lodash', 'backbone'],

function($, _, Backbone) {

    var Room = Backbone.Model.extend({
        urlRoot: "rooms/",
        //urlRoot: "room",
		//idAttribute: "_id",

/*        methodToURL: {
            'read': '/user/get',
            'create': '/user/create',
            'update': '/rooms/update',
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
                options.url = model.urlRoot + 'delete?roomId=' + model.id;       

              } else {
                 //options.url = model.urlRoot + 'update?roomId='+model.id;
                 options.url = model.urlRoot + 'update'; 
              }
              return Backbone.sync(method, model, options);
        },

        defaults: {
            "id": null,
            "number": "",
            "area": "",
            "windows": "",
      			"validationDate": "",
      			"picture": ""
			
        }
    });

    return Room;
});