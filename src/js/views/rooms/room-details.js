define(
['jquery', 'lodash', 'backbone', 'utils/tpl'],

function($, _, Backbone, tpl) {

    var RoomView = Backbone.View.extend({

        tagName: "div",
        // Not required since 'div' is the default if no el or tagName specified


        initialize: function() {

            this.template = _.template(tpl.get('room-details'));
            this.model.bind("change", this.render, this); //this lined has been commented out for debugging purpose
        },

        render: function(eventName) {
            this.$el.html(this.template(this.model.toJSON()));
            return this.el;
        },

        events: {
            "change input": "change",
            "click .save": "saveRoom",
            //"submit .room-details-form": "saveRoom",
            //"click .save": "beforeSave",
            "click .delete": "deleteRoom",
            "change .upload": "displayPicture",
            "click .imageClass": "clickImage"
        },

        change: function(event) {
            var target = event.target;
            //alert("there is something changed!!");
            console.log('changing ' + target.id + ' from: ' + target.defaultValue + ' to: ' + target.value);
            // You could change your model on the spot, like this:
            var change = {};
            change[target.name] = target.value;
            this.model.set(change);
        },


        beforeSave: function(){
            var self = this;
            if (this.pictureFile) {
            this.model.set("picture", this.pictureFile.name);
            self.uploadFile(this.pictureFile,
                function () {
                    self.saveRoom();
                }
            );
        } else {
            this.saveRoom();
        }
        return false;

        },



        saveRoom1: function(ev) {
            //var roomDetails = $(ev.currentTarget).serializeObject();
            var roomDetails = $(ev.currentTarget)
            console.log(roomDetails);
            return false;
            //ev.preventDefault();
        },


        saveRoom: function() {
            
/*            this.model.set({				
                firstName: $('#firstName').val(),
                surname: $('#surname').val(),
                gender: $('#gender').val(),
                age: $('#age').val(),
                phoneNumber: $('#phoneNumber').val(),
                email: $('#email').val(),
				registerDate: $('#registerDate').val(),
                description:$('#description').val(),
                //picture: $('#browse').val()
                picture: this.pictureFile.name
            });*/
            if (this.model.isNew()) {
                var self = this;
                app.roomList.create(this.model, { wait: true,
                    //app.roomList.create(this.model.attributes, { wait: true,
                    //app.roomList.create(this.model.toJSON(), { wait: true, 
                   // this.model.save(null, { wait: true,     
                    success: function() {
						alert("you have registered a new room!!!  ");						
                        app.navigate('rooms/' + self.model.id, false);
						
                    }
                });
            } else {
                var self = this;
                this.model.save({ wait: true,
                    success: function() {
                        alert("you have Changed the room!!!  ");                     
                        app.navigate('rooms/' + self.model.id, false);
                        
                    }
                });
            }

            return false;
        },

        uploadFile: function (file, callbackSuccess) {
            var self = this;
            var data = new FormData();
            data.append('file', file);
            $.ajax({
                url: 'uploadPicture',
                type: 'POST',
                data: data,
                processData: false,
                cache: false,
                contentType: false
            })
            .done(function () {
                console.log(file.name + " uploaded successfully");
                callbackSuccess();
            })
            .fail(function () {
                self.showAlert('Error!', 'An error occurred while uploading ' + file.name, 'alert-error');
            });
        },

        deleteRoom: function(ev) {
            this.model.destroy({
                success: function() {
                    alert('Room deleted successfullYYy');
                    //router.navigate('',{trigger: true});
                    window.history.back();
                }
            });
            return false;
        },

        displayPicture: function(evt){
            alert("here is the pic !!");
            var files = evt.target.files;
            if (files) {
                this.pictureFile = files[0];
                var reader = new FileReader();
//this block works for preloading the image
/*                reader.onload = function(e){
                    $('#img_prev').attr('src',e.target.result).width(200).height(200);
                    $(".imageClass").css({"background-size":  "200px 200px", "background-image": "url(" + e.target.result + ")"});*/
                reader.onloadend = function(){   
                    $('#img_prev').attr('src',reader.result).width(200).height(200);
                    
                };
                reader.readAsDataURL(this.pictureFile);
            } else {
                this.pictureFile = this.value;
                changeimg(pictureFile);
            }

        },

        clickImage: function(){
                document.getElementById('browse').click();
        }


    });

    return RoomView;


});




