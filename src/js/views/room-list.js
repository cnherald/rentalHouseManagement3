define(
['jquery', 'lodash', 'backbone', 'utils/tpl'],

function($, _, Backbone, tpl) {

    var RoomListView = Backbone.View.extend({

        tagName: 'ul',

        initialize: function() {
            this.model.bind("reset", this.render, this);
            this.model.bind("add", this.appendNewRoom, this);
        },

        render: function(eventName) {
            _.each(this.model.models, function(room) {
                this.appendNewRoom(room);
            }, this);
            return this.el;
        },

        appendNewroom: function(room) {
            this.$el.append(new RoomListItemView({
                model: room
            }).render());
        }
    });

    var RoomListItemView = Backbone.View.extend({

        tagName: "li",
		events:{
			"click #roomFirstName": "alertMsg"
		},
        initialize: function() {
            this.template = _.template(tpl.get('room-list-item'));
            this.model.bind("change", this.render, this);
            this.model.bind("destroy", this.close, this);
        },
		alertMsg: function(){
			//alert("test!!!!");
			//app.navigate('rooms/' + this.model.id, true); 
			//return false;
		},
        render: function(eventName) {
            this.$el.html(this.template(this.model.toJSON()));
            return this.el;
        }

    });

    return RoomListView;

});