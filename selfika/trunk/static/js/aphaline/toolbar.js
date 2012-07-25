Aphaline.Toolbar = (function() {
    
	PATH = '/static/images/aphaline/'
	
	/*
     * Panel button
     */
    var Button = function(name, caption, callback) {

        this.name = name;
        this.caption = caption;
        this.callback = callback;

        this.disabled = false;
        this.activated = false;
        this.hidden = true;

        this.dom = $(' \
            <div class="aph-toolbar-button">    \
                <div class="img"></div>         \
                <div class="caption"></div>     \
            </div>                              \
        ');

        this.dom.find('.img').append(
            '<img src="'+PATH+'/toolbar/' + this.name + '.png" \
                  alt="' + this.caption + '" />'
        );
        this.dom.find('.caption').text(this.caption);
        this.dom.click(function(b) {
            return function(evt) {
                if (!b.disabled) 
                    return b.callback(evt);
            }
        }(this));

    };

    Button.prototype.enable = function() {
        this.dom.removeClass('disabled');
        this.disabled = false;
        return this;
    }
    Button.prototype.disable = function() {
        this.dom.addClass('disabled');
        this.disabled = true;
        return this;
    }
    Button.prototype.activate = function() {
        this.dom.addClass('activated');
        this.activated = true;
        return this;
    }
    Button.prototype.deactivate = function() {
        this.dom.removeClass('activated');
        this.activated = false;
        return this;
    }
    Button.prototype.show = function() {
        this.dom.show();
        this.hidden = false;
        return this;
    }
    Button.prototype.hide = function() {
        this.dom.hide();
        this.hidden = true;
        return this;
    }
    Button.prototype.destroy = function() {
        this.dom.remove();
        return null;
    }

    /*
     * Panel
     */
    var Panel = function(name) {
        this.name = name;
        this.disabled = false;
        this.hidden = true;
        this.buttons = {};
        this.dom = $(' \
            <div class="aph-toolbar-panel">     \
                <div class="buttons"></div>     \
            </div>                              \
        ');
    };

    Panel.prototype.createButton = function(name, caption, callback) {
        var button = new Button(name, caption, callback);
        this.addButton(button);
        return this;
    }
    Panel.prototype.addButton = function(button) {
        this.buttons[button.name] = button;
        this.dom.find('.buttons').append(button.dom);
        return this;
    }
    Panel.prototype.removeButton = function(name) {
        if (this.buttons[name]) {
            this.buttons[name].destroy();
            delete this.buttons[name];
        }
        return this;
    }
    Panel.prototype.getButton = function(name) {
        return this.buttons[name];
    }
    Panel.prototype.enable = function() {
        this.dom.removeClass('disabled');
        this.disabled = false;
        return this;
    }
    Panel.prototype.disable = function() {
        this.dom.addClass('disabled');
        this.disabled = true;
        return this;
    }
    Panel.prototype.enableAll = function() {
        for (var i in this.buttons)
            this.buttons[i].enable();
        this.enable();
        return this;
    }    
    Panel.prototype.disableAll = function() {
        for (var i in this.buttons) {
        	this.buttons[i].disable();
        	this.buttons[i].deactivate();
        }
        this.disable();
        return this;
    }    
    Panel.prototype.deactivateAll = function() {
        for (var i in this.buttons) {
        	this.buttons[i].deactivate();
        }
        return this;
    }    
    Panel.prototype.show = function() {
        this.dom.show();
        this.hidden = false;
        return this;
    }
    Panel.prototype.hide = function() {
        this.dom.hide();
        this.hidden = true;
        return this;
    }
    Panel.prototype.showAll = function() {
        for (var i in this.buttons)
            this.buttons[i].show();
        this.show();
        return this;
    }    
    Panel.prototype.hideAll = function() {
        for (var i in this.buttons)
            this.buttons[i].hide();
        this.hide();
        return this;
    }    
    Panel.prototype.destroy = function() {
        for (var i in this.buttons)
            this.buttons[i].destroy();
        this.dom.remove();
        return null;
    }

    var dom = $('<div id="aph-toolbar"><div class="wrapper"></div></div>');
    var panels = {}

    $('body').append(dom);

    /*
     * Toolbar itself ;)
     */
    return {

        Button: Button,
        Panel: Panel,

        createPanel: function(name) {
            var panel = new Panel(name);
            panels[name] = panel;
            dom.find('.wrapper').append(panel.dom);
            return panel;
        },
        removePanel: function(name) {
            if (panels[name]) {
                panels[name].destroy();
            }
            delete panels[name];
        },
        getPanel: function(name) {
            return panels[name];
        }
    }

})();