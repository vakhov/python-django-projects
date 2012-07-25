/*
 * Aphaline API
 */
Aphaline.API = {

    /* Core */
    Core: {
        variants_available: function() {
            return [
                { 'name': 'default', 'caption': 'Просмотр' }, 
                { 'name': 'edit', 'caption': 'Редактирование' }
            ]
        }  
    },

    /* Widgets */

    Widgets: {
        list: function() {
            var result = null;
            $.ajax({
                async: false,
                type: 'GET',
                url: '/api/widgets/list/',
                dataType: 'json',
                processData: false,
                success: function(reply) {
                    result = reply;
                }
            });
            return result;
        },
        create: function(widget_type, zone_id, order, callback) {
            $.get(
                '/api/widgets/create/' + widget_type + '/',
                {
                    //v: 'apiedit',
                    zone_id: zone_id,
                    order: order
                },
                callback
            );
        },
        move: function(widget_id, zone_id, order, callback) {
            $.get(
                '/api/widgets/move/' + widget_id + '/',
                {
                    zone_id: zone_id,
                    order: order
                },
                callback
            );
        },
        delete: function(widget_id, callback) {
            $.get('/api/widgets/delete/' + widget_id + '/', callback);
        }
    },
    
    Legacy: {
    	form: function(model, id, data, callback, errback) {
    		if (id)
    			var url = '/api/aphaline/' + model + '/form/' + id + '/'
			else
				var url = '/api/aphaline/' + model + '/form/'
			var response = null;
    		$.ajax({
    			async: false,
    			type: 'POST',
    			url: url,
    			data: data,
    			//processData: false,
    			success: function(reply) {
    				if (reply.error && errback) errback(reply.error); 
    				else if (callback) callback(reply);
    				response = reply;
    			},
    			error: function(a, e) {
    				if (errback) errback({message: 'ParseError'});
    				return false;
    			}
    		});
    		return response;
    	},
    	delete: function(model, id, callback, errback) {
			var url = '/api/aphaline/' + model + '/delete/' + id + '/'
			var response = null;
    		$.ajax({
    			async: false,
    			type: 'POST',
    			url: url,
    			processData: false,
    			success: function(reply) {
    				if (reply.error && errback) errback(reply.error); 
    				else if (callback) callback(reply);
    				response = reply;
    			},
    			error: function(a, e) {
    				if (errback) errback({message: 'ParseError'});
    				return false;
    			}
    		});
    		return response;    		
    	}
    }

    /* Nothing more yet... */

}