/*
 * Interface and event handling
 */
Aphaline.Interface = (function() {

    var selected_widget = null;
    var selected_adder = null;

    var is_move_mode = false;

    var aph_adder = '<div class="aph-widget-adder"><div></div></div>';
    var aph_widget = '<div class="aph-widget"></div>';

    var global_panel = null;
    var variants_panel = null;
    var widget_panel = null;

    // Simple actions

    var selectWidget = function(widget_obj) {
        widget_obj.addClass('selected');
        selected_widget = widget_obj;
        widget_panel.showAll();
    }

    var deselectWidget = function() {
        if (selected_widget == null)
            return;
        selected_widget.removeClass('selected');
        selected_widget = null;
        widget_panel.hide();                
    }

    var selectAdder = function(adder_obj) {
        adder_obj.addClass('selected');
        selected_adder = adder_obj;
    }

    var deselectAdder = function() {
        if (selected_adder == null)
            return;
        selected_adder.removeClass('selected')
        selected_adder = null;
    }

    var enterMoveMode = function() {
        $('.aph-widget-adder').addClass('movemode');
        selected_widget.prev('.aph-widget-adder').removeClass('movemode').addClass('invisible');
        selected_widget.next('.aph-widget-adder').removeClass('movemode').addClass('invisible');
        selected_widget.find('.aph-widget-adder').removeClass('movemode').addClass('invisible');
        is_move_mode = true;
        return false;
    }

    var leaveMoveMode = function() {
        $('.aph-widget-adder').removeClass('movemode').removeClass('invisible');
        is_move_mode = false;
        return false;
    }

    /*
     * Event handlers
     */

    // Widgets

    var widgetClickHandler = function(evt) {
        if (is_move_mode)
            leaveMoveMode();
        deselectAdder();
        var target = $(evt.currentTarget);
        if (selected_widget == null) {
            // No widget selected yet
            selectWidget(target);
        }
        else if (target[0] == selected_widget[0]) {
            // This widget is already selected
            deselectWidget(target);
        }
        else {
            // Another widget is selected
            deselectWidget(selected_widget);
            selectWidget(target);
        }
        return false;
    }

    var widgetDblClickHandler = function(evt) {
        if (is_move_mode)
            leaveMoveMode();
        deselectAdder();
        var target = $(evt.currentTarget);
        if (selected_widget == null) {
            selectWidget(target);
        }
        Aphaline.Actions.editWidget();
        return false;
    }

    var widgetMouseHandler = function(evt) {
        if (selected_adder == null) {
            var target = $(evt.currentTarget);
            if (evt.type == 'mouseover') {
                target.addClass('hover');
            }
            else {
                target.removeClass('hover');
            }
            return false;
        }
    }

    // Adders

    var adderClickHandler = function(evt) {
        
        /* Moving widget */
        if (is_move_mode) {
            var target = $(evt.currentTarget);
            Aphaline.Actions.moveWidget(target);
            deselectWidget();
            leaveMoveMode();
        }

        /* Showing "adder" menu */
        else {
            deselectWidget();
            var target = $(evt.currentTarget);
            selectAdder(target);
            target.removeClass('hover');
            Aphaline.WidgetList.show(evt.pageX, evt.pageY);
        }
        return false;
    }

    var adderMouseHandler = function(evt) {
        if (selected_adder == null) {
            if (evt.type == 'mouseover') {
                var target = $(evt.currentTarget);
                target.siblings('.aph-widget-adder').removeClass('hover');
                target.addClass('hover');
            }
            else {
                var target = $(evt.currentTarget);
                target.removeClass('hover');                    
            }
        }
    }

    // Common interface handlers

    var commonClickHandler = function(evt) {
        if (selected_adder != null) {
            Aphaline.WidgetList.hide();
            deselectAdder();
        }
    }

    var outsideClickHandler = function() {
        if (is_move_mode)
            leaveMoveMode();
        Aphaline.WidgetList.hide();
        deselectWidget();
        deselectAdder();
    }

    var zoneMouseHandler = function(evt) {
        if (selected_adder == null) {
            var target = $(evt.currentTarget);
            if (evt.type == 'mouseover') {
                target.addClass('hover');
            }
            else {
                target.removeClass('hover');
            }
        }
    }

    var commonKeypressHandler = function(evt) {
        // Deleting widet by "delete" key
        if (evt.keyCode == 46 && selected_widget != null) {
            return Aphaline.Actions.deleteWidget();
        }
    }

    // List item click handler (adding widget)
    
    var listItemClickHandler = function(evt, item) {
        var zone = selected_adder.parent('.aph-zone').eq(0);
        //var zone_type = zone.attr('aph-zone-id');
        //var zone_pid = zone.attr('aph-zone-pid');
        //var zone_sid = zone.attr('aph-zone-sid');
        var zone_id = zone.attr('aph-zone-id');
        var order = 1 + zone.children('.aph-widget-adder').index(selected_adder);
        //Aphaline.Actions.createWidget(selected_adder, item.name, zone_type, zone_pid, zone_sid, order);
        Aphaline.Actions.createWidget(selected_adder, item.name, zone_id, order);
        return false;
    }

    // Toolbar initialization
    var initToolbar = function() {
        // Creating panels
        globals_panel = Aphaline.Toolbar.createPanel('globals');
        structure_panel = Aphaline.Toolbar.createPanel('structure');
        variants_panel = Aphaline.Toolbar.createPanel('variants');
        widget_panel = Aphaline.Toolbar.createPanel('widget');

        // Creating default buttons
        globals_panel
            .createButton('quit', 'Выход', Aphaline.Actions.quit)
            .showAll()
        ;

        structure_panel
	        .createButton('structure', 'Структура сайта', Aphaline.Actions.toggleStructure)
	        .showAll()
	    ;
        
        // Creating buttons for available view variants
        var variants = Aphaline.API.Core.variants_available();
        for (var i in variants) {
            // Preparing
            var variant = variants[i];
            var old_addr = window.location.href.replace(/\?.*/, '');
            var addr = old_addr + '?v=' + variant.name;
            var callback = function(addr) { return function() {
                window.location.href = addr;
            } } (addr);
            var prefixed_name = 'v_' + variant.name;
            // Creating the button
            variants_panel.createButton(prefixed_name, variant.caption, callback);
            // Disabling the button with current variant
            // if (gup('v') == variant.name || (gup('v') == '' && variant.name == 'default'))
            //     variants_panel.getButton(prefixed_name).disable();
        }
        if ($.cookie('aphaline_edit_mode') != 1)
            variants_panel.getButton('v_default').activate();
        else
            variants_panel.getButton('v_edit').activate();
        
        variants_panel.showAll();

        // Buttons for widgets editing
        widget_panel
            .createButton('edit', 'Редактировать', Aphaline.Actions.editWidget)
            .createButton('move', 'Переместить', enterMoveMode)
            .createButton('delete', 'Удалить', Aphaline.Actions.deleteWidget)
        ;

    }

    /*
     * The final object
     */

    return {
        init: function() {
            // Make a border for zones
            $('[aph-zone-id]').addClass('aph-zone')
            // Render adders
            $('[aph-zone-id]').append(aph_adder);
            $('[aph-widget-type]').before(aph_adder);
            // Render widgets
            $('[aph-widget-type]').wrap(aph_widget);
            // Handle events
            $('body')
                .bind('widgetlist_item_click', listItemClickHandler)
                .bind('click', commonClickHandler)
                .delegate('.aph-widget', 'click' , widgetClickHandler)
                .delegate('.aph-widget', 'dblclick' , widgetDblClickHandler)
                .delegate('.aph-widget-adder', 'click', adderClickHandler)
                .delegate('.aph-widget', 'mouseover mouseout', widgetMouseHandler)
                .delegate('.aph-zone', 'mouseover mouseout', zoneMouseHandler)
            ;
            $('[aph-zone-id]')
                .delegate('.aph-widget-adder', 'mouseover mouseout', adderMouseHandler)
            ;
            $(window)
                .bind('click', outsideClickHandler)
                .bind('keypress', commonKeypressHandler)
            ;
            // Initializing toolbar
            initToolbar();
        },

        update: function() {
            deselectWidget();
            deselectAdder();
            $('[aph-zone-id]').each(function() {
                if (!$(this).hasClass('aph-zone')) {
                    $(this).addClass('aph-zone');
                    $(this).append(aph_adder);
                    $(this).find('[aph-widget-type]')
                        .before(aph_adder)
                        .wrap(aph_widget)
                    ;
                }
            });
        },

        selectWidget: selectWidget,
        deselectWidget: deselectWidget,
        selectAdder: selectAdder,
        deselectAdder: deselectAdder,

        enterMoveMode: enterMoveMode,
        leaveMoveMode: leaveMoveMode,
        
        getSelectedAdder: function() {
            return selected_adder;
        },
        getSelectedWidget: function() {
            return selected_widget;
        }
    }
            
})();