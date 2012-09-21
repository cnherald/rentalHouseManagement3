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
            console.log('changing ' + target.id + ' from: ' + target.defaultValue + ' to: ' + target.value);
            // You could change your model on the spot, like this:
            // var change = {};
            // change[target.name] = target.value;
            // this.model.set(change);
        },

        saveTenant: function() {
            this.model.set({
                FirstName: $('#firstName').val(),
                Surname: $('#surname').val(),
                Gender: $('#gender').val(),
                Age: $('#age').val(),
                PhoneNumber: $('#phoneNumber').val(),
                Email: $('#email').val()
            });
            if (this.model.isNew()) {
                var self = this;
                app.tenantList.create(this.model, {
                    success: function() {
                        //app.navigate('tenants/' + self.model.id, false);
						app.navigate('tenants/' + self.model.FirstName, false);
                    }
                });
            } else {
                this.model.save();
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