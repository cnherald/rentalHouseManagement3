define(
['jquery', 'lodash', 'backbone', 'models/rooms/room-model'],

function($, _, Backbone, Room) {

	var RoomCollection = Backbone.Collection.extend({
		model: Room,
		url: "rooms/"
	});

	return RoomCollection;
});