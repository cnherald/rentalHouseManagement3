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
            "click .delete": "deleteTenant"
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
        }

    });

    return TenantView;

//(".upload").change(function () {


},

function handleFileSelect(evt) {
    alert("SSssssssssssss");
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
},

document.getElementById('browse').addEventListener('change', handleFileSelect, false)



// $(".upload").change(function () {
//     alert("SSssssssssssss");
//     var fileObj = this,
//         file;
    
//     if (fileObj.files) {
//         file = fileObj.files[0];
//         var fr = new FileReader;
//         fr.onloadend = changeimg;
//         fr.readAsDataURL(file)
//     } else {
//         file = fileObj.value;
//         changeimg(file);
//     }
// }),

// function onbrowse() {
//     document.getElementById('browse').click();
// },


// function changeimg(str) {
//     if(typeof str === "object") {
//         str = str.target.result; // file reader
//     }
    
//     $(".unknown").css({"background-size":  "100px 100px",
//                        "background-image": "url(" + str + ")"});
// }


// function handleFileSelect(evt) {
//     var files = evt.target.files; // FileList object

//     // Loop through the FileList and render image files as thumbnails.
//     for (var i = 0, f; f = files[i]; i++) {

//       // Only process image files.
//       if (!f.type.match('image.*')) {
//         continue;
//       }

//       var reader = new FileReader();

//       // Closure to capture the file information.
//       reader.onload = (function(theFile) {
//         return function(e) {
//           // Render thumbnail.
//           var span = document.createElement('span');
//           span.innerHTML = ['<img class="thumb" src="', e.target.result,
//                             '" title="', escape(theFile.name), '"/>'].join('');
//           document.getElementById('list').insertBefore(span, null);
//         };
//       })(f);

//       // Read in the image file as a data URL.
//       reader.readAsDataURL(f);
//     }
//   },

//   document.getElementById('files').addEventListener('change', handleFileSelect, false)


);

 
 
 



