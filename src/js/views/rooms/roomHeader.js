define(
['jquery', 'lodash', 'backbone', 'utils/tpl'],

function($, _, Backbone, tpl) {

    var roomHeaderView = Backbone.View.extend({

        initialize: function() {
            this.template = _.template(tpl.get('roomHeader'));
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

    return roomHeaderView;

});