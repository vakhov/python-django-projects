if (!Aphaline) Aphaline = {};

/*
 * Adder "menu": widgets and groups list
 */

Aphaline.WidgetList = (function() {
    
    var repr = null;
    var typeset = null;
    var last_widget = null;

    var getWidgetTypeset = function() {
        // Retrieves widget groups and classes from the server
        return Aphaline.API.Widgets.list();
    };

    var clean = function() {
        repr.empty();
    }

    var addItem = function(item, clazz) {
        if (item == null) {
            // empty "last widget" case
            return;
        }
        var obj = $('<li></li>');
        obj
            .addClass('item')
            .attr('title', item.name)
            .text(item.title)
            .data('meta', item)
        ;
        if (clazz) {
            obj.addClass(clazz);
        }
        repr.append(obj);
    }

    var addGroup = function(group) {
        var obj = $('<li></li>');
        obj
            .addClass('group')
            .attr('title', group.slug)
            .text(group.group)
            .data('meta', group)
        ;
        repr.append(obj);
    }

    var addBackButton = function() {
        var obj = $('<li></li>');
        obj
            .addClass('back')
            .attr('title', 'Назад')
            .text('Назад')
        ;
        repr.append(obj);
    }

    var renderIndex = function() {
        clean();
        addItem(last_widget, 'last_widget');
        for (var i in typeset)
            addGroup(typeset[i]);
        return false;
    }

    var renderSub = function(group) {
        clean();
        addBackButton();
        for (var i in group.items)
            addItem(group.items[i]);
        return false;
    }

    var setLastWidget = function(widget) {
        last_widget = widget;
        $.cookie('last_widget_name', widget.name);
        $.cookie('last_widget_title', widget.title);
    }

    var itemClickHandler = function(evt) {
        var item = $(evt.target).data().meta;
        setLastWidget(item);
        // Item click event handling is external
        $('body').trigger('widgetlist_item_click', item);
        Aphaline.WidgetList.hide();
        return false;
    }

    var groupClickHandler = function(evt) {
        var group = $(evt.target).data().meta;
        renderSub(group);
        return false;
    }

    return {
        init: function() {
            // Getting typeset
            typeset = getWidgetTypeset();
            // Creating the window
            repr = $('<ul></ul>');
            repr
                .attr('id', 'aph-widget-adder-window')
                // Binding events
                .delegate('.item',  'click', itemClickHandler)
                .delegate('.group', 'click', groupClickHandler)
                .delegate('.back',  'click', renderIndex)
            ;
            if ($.cookie('last_widget_name')) {
                last_widget = {
                    name: $.cookie('last_widget_name'),
                    title: $.cookie('last_widget_title')
                }
            }
            // Inserting the window to the body
            $('body').append(repr);
        },
        show: function(x, y) {
            // Checks if initialised
            if (!repr)
                this.init();
            // Constructs the list...
            renderIndex();
            // ... and shows the window in given position

            var position = {}

            position.top = y + 10 + 'px';
            position.left = x + 10 + 'px';
            
            // if ($('#container').height() < 400 || 
            //     y < $('#container').height() - 400) 
            // {
            //     position.top = y + 10 + 'px';
            //     position.bottom = 'auto';
            // }
            // else {
            //     position.bottom = $('#container').height() - y + 10 + 'px';
            //     position.top = 'auto';
            // }

            // if (x < $('#container').width() - 250) {
            //     position.left = x + 10 + 'px';
            //     position.right = 'auto';
            // }
            // else {
            //     position.right = $('#container').width() - x - 10 + 'px';
            //     position.left = 'auto';
            // }

            repr
                .css(position)
                .show()
            ;

        },
        hide: function() {
            if (!repr) 
                return;
            else 
                repr.hide();
        }
    }

})()