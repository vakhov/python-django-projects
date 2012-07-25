Aphaline.Actions = {
    
    createWidget: function(selected_adder, name, zone_id, order) {
        var callback = function(data) {
            var new_element = $(data);
            var aph_adder = '<div class="aph-widget-adder"><div></div></div>';
            var aph_widget = '<div class="aph-widget"></div>';
            new_element.find('[aph-zone-id]').addClass('aph-zone').append(aph_adder);
            selected_adder
                .after(aph_adder)
                .before(aph_adder)
                .wrap(aph_widget)
                .replaceWith(new_element)
            ;
            Aphaline.Interface.deselectAdder();
            Aphaline.Interface.selectWidget(new_element.parent());
            Aphaline.Actions.editWidget();
        }
        Aphaline.API.Widgets.create(name, zone_id, order, callback);
        return false;
    },

    editWidget: function() {
        var widget = Aphaline.Interface.getSelectedWidget();
        Aphaline.Editor.openWidgetForm(widget);
    },

    moveWidget: function(item) {
        
        var widget = Aphaline.Interface.getSelectedWidget();

        var widget_id = widget.children('[aph-widget-id]').attr('aph-widget-id');
        var zone = item.parent('.aph-zone');
        var zone_id = zone.attr('aph-zone-id');
        var order = 1 + zone.children('.aph-widget-adder').index(item);

        var same_zone = item.siblings('.aph-widget.selected')[0];

        if (item.prevAll('.aph-widget.selected')[0])
            order--;
        
        var callback = function() {
            var aph_adder = '<div class="aph-widget-adder"><div></div></div>';
            if (same_zone) {
                item.before(widget);
                zone.children('.aph-widget-adder').remove();
                zone.append(aph_adder);
                zone.children('.aph-widget').before(aph_adder);
            }
            else {
                var start_zone = widget.parent('.aph-zone');
                item.before(widget);
                zone.children('.aph-widget-adder').remove();
                zone.append(aph_adder);
                zone.children('.aph-widget').before(aph_adder);
                start_zone.children('.aph-widget-adder').remove();
                start_zone.append(aph_adder);
                start_zone.children('.aph-widget').before(aph_adder);
            }
        }

        Aphaline.API.Widgets.move(widget_id, zone_id, order, callback);
        
    },

    deleteWidget: function() {
        selected_widget = Aphaline.Interface.getSelectedWidget();
        if (confirm("Are you sure?")) {
            var id = selected_widget.children('[aph-widget-id]').attr('aph-widget-id');
            var callback = function() {
                var widget_to_delete = selected_widget; 
                Aphaline.Interface.deselectWidget();
                $(widget_to_delete).prev('.aph-widget-adder').remove();
                $(widget_to_delete).remove();
            }
            Aphaline.API.Widgets.delete(id, callback);
        }
        return false;
    },

    /*
     * Structure
     */

    toggleStructure: function() {
        window.location.href = '/api/structure/admin/';
    },

    /*
     * Other
     */

   quit: function() {
        window.location.href = '/logout/';
        return false;
    }

}