define(
['jquery', 'lodash', 'backbone', 'utils/tpl'],

function($, _, Backbone, tpl) {

    var TenantView = Backbone.View.extend({

        tagName: "div",
        // Not required since 'div' is the default if no el or tagName specified
        initialize: function() {

            this.template = _.template(tpl.get('tenant-details'));
            this.model.bind("change", this.render, this);
        },

        render: function(eventName) {
            this.$el.html(this.template(this.model.toJSON()));
            return this.el;
        },

        events: {
            "change input": "change",
            "click .save": "saveTenant",
            "click .delete": "deleteTenant",
            "change .upload": "loadFile"
        },

        change: function(event) {
            var target = event.target;
            //alert("there is something changed!!");
            console.log('changing ' + target.id + ' from: ' + target.defaultValue + ' to: ' + target.value);
            // You could change your model on the spot, like this:
            // var change = {};
            // change[target.name] = target.value;
            // this.model.set(change);
        },

        saveTenant: function() {
            this.model.set({				
                firstName: $('#firstName').val(),
                surname: $('#surname').val(),
                gender: $('#gender').val(),
                age: $('#age').val(),
                phoneNumber: $('#phoneNumber').val(),
                email: $('#email').val(),
				registerDate: $('#registerDate').val(),
                picture: $('#img').val()
            });
            if (this.model.isNew()) {
                var self = this;
                app.tenantList.create(this.model, { wait: true,
                    success: function() {
						alert("you have registered a new tenant!!!  ");						
                        app.navigate('tenants/' + self.model.id, false);
						
                    }
                });
            } else {
                this.model.save(this.model, { wait: true,
                    success: function() {
                        alert("you have Changed the tenant!!!  ");                     
                        app.navigate('tenants/' + self.model.id, false);
                        
                    }
                });
            }

            return false;
        },

        deleteTenant: function() {
            this.model.destroy({
                success: function() {
                    alert('Tenant deleted successfully');
                    window.history.back();
                }
            });
            return false;
        },

        loadFile: function(evt){
            alert("here is the pic !!");
            var files = evt.target.files;
            if (files) {
                file = files[0];
                /*var fr = new FileReader();*/
 /*               fr.onloadend = function(aImg){
                    aImg=aImg.target.result;

                };*/
/*                fr.onloadend = changeimg(ttt);
                fr.readAsDataURL(file);*/
                // var img = document.createElement﻿("img");
                // img.classList.add("obj");
                // img.file = file﻿;
                //preview.appendChild﻿(img);
                var reader = new FileReader();
                // reader.onloadend ﻿= (function(aImg﻿) {
                //      return function(e) { 
                //         aImg.src = e.target.result; 

                //       $(".unknown").css({"background-size":  "100px 100px", "background-image": "url(" + aImg﻿ + ")"});
                //      };
                     

                //       }﻿)(file);﻿
                //reader.onload = changeimg1;
                reader.onloadend = function(e){
                    $('#img_prev').attr('src',e.target.result).width(150).height(200);
                };
                reader.readAsDataURL(file);
            } else {
                file = this.value;
                changeimg(file);
            }

        }



        // changeimg: function (str) {
        //     if(typeof str === "object") {
        //             str = str.target.result; // file reader
        //         }
                
        //         $(".unknown").css({"background-size":  "100px 100px",
        //                            "background-image": "url(" + str + ")"});
        // }

        // changeimg1: function(e){
        //     $('#img_prev').attr('src',e.target.result).width(150).height(200);
        // },

    });

    return TenantView;




//(".upload").change(function () {





});


 //$(".upload").change(function () {

/*$("#browse").change(function()){
    alert("here is the pic !!");
    var fileObj = this,
        file;
    
    if (fileObj.files) {
        file = fileObj.files[0];
        var fr = new FileReader;
        fr.onloadend = changeimg;
        fr.readAsDataURL(file)
    } else {
        file = fileObj.value;
        changeimg(file);
    }
});

function onbrowse() {
    document.getElementById('browse').click();
}

function changeimg(str) {
    if(typeof str === "object") {
        str = str.target.result; // file reader
    }
    
    $(".unknown").css({"background-size":  "100px 100px",
                       "background-image": "url(" + str + ")"});
}
*/


