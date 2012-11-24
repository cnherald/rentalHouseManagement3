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
				registerDate: $('#registerDate').val()
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

});