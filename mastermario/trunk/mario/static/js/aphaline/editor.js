Aphaline.Editor = (function() {
    
    var w = $('\
        <div id="aph-editor">                   \
            <div class="aph-wrapper">            \
                <div class="aph-header">        \
                    Редактирование              \
                </div>                          \
                <div class="aph-x">X</div>          \
                <div class="aph-container"></div>   \
            </div>                              \
        </div>                                  \
    ');

    var shadow = $('<div id="aph-shadow"></div>');

    var header = w.find('.aph-header');
    var x = w.find('.aph-x');
    var container = w.find('.aph-container');

    $('body').append(w);
    $('body').append(shadow);

    var selected_widget = null;

    var empty = function() {
        editing_widget = null;
        container.empty();
    }
    var load = function(url) {
        container.load(url);
    }
    var show = function() {
        shadow.show();
        w.show();
        selected_widget = Aphaline.Interface.getSelectedWidget();
        return false;
    }
    var hide = function() {
        shadow.hide();
        w.hide();
        return false;
    }   

    container.delegate('input[type=submit][name="submit_legacy"]', 'click', function() {
        container.find('form').ajaxSubmit(function(data) {
        	window.location.reload();
        });
        return false;
    });

    container.delegate('input[type=submit][name="submit_widget_form"]', 'click', function() {
        container.find('form').ajaxSubmit(function(data) {
            $(selected_widget).html(data);
            Aphaline.Interface.update();
            hide();
        });
        return false;
    });

    container.delegate('input[type=button][name="submit_and_add_widget"]', 'click', function() {
        container.find('form').ajaxSubmit(function(data) {
            $(selected_widget).html(data);
            Aphaline.Interface.update();
            hide();
            var selected_adder = $(selected_widget).next('.aph-widget-adder');
            var zone = selected_adder.parent('.aph-zone');
            var zone_id = zone.attr('aph-zone-id');
            var order = 1 + zone.children('.aph-widget-adder').index(selected_adder);
            var name = $(selected_widget).find('[aph-widget-type]').attr('aph-widget-type');
            Aphaline.Actions.createWidget(selected_adder, name, zone_id, order);
        });
        return false;
    });

    x.click(function() {
        hide();
        return false;
    });

    shadow.click(function() { return false });

    var editing_widget = null;

    return {
        openWidgetForm: function(widget, title) {
            hide();
            empty();
            editing_widget = widget;
            title = title || 'Редактирование';
            header.text(title);
            var widget_id = widget.children('[aph-widget-id]').attr('aph-widget-id');
            var url = '/api/widgets/form/'+widget_id+'/';
            container.load(url, show);
        },
        openContent: function(content, title) {
        	hide();
        	empty();
        	editing_widget = null;
            title = title || 'Редактирование';
            header.text(title);
            container.html(content);
            show();
        }
    }

})();