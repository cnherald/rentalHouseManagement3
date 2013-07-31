define(
['jquery', 'lodash', 'backbone', 'utils/tpl'],

function($, _, Backbone, tpl) {

    var HeaderView = Backbone.View.extend({

        initialize: function() {
            this.template = _.template(tpl.get('header'));
        },

        render: function(eventName) {
            this.$el.html(this.template());
            return this.el;
        },

        events: {
            "click .new": "newRoom"
        },

        newRoom: function(event) {
            app.navigate("room/new", true);
            return false;
        }

    });

    return HeaderView;

});