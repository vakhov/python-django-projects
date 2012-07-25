var Colored = Base.extend({
    constructor: function(items){
        this._selectedClass = "selected";
        this._items = items;
        this._body = $("body");
        this._defaultClass = "colored_green";

        this._loaderId = [];
        this._loaderInterval = 500;
        this._loaderDelta = 300;
    },
    init: function(){
        var _this = this;
        var savedClass = $.cookie("coloredClass") != null ? $.cookie("coloredClass") : this._defaultClass;
        this._body.addClass(savedClass);
        this._items.each(function(){
            if ($(this).attr("rel") == savedClass) {
                _this.addSelected($(this).parent());
            }
            _this.registerHandlers($(this));
        });
    },
    registerHandlers: function(item){
        var li = item.parent();
        var _this = this;
        item.click(function(){
            if (!_this.isSelected(li)) {
                _this.removeSelected();
                _this.cleanColoredClass();
                _this.addSelected(li);
                _this.setColoredClass(item);
            }
            return false;
        });
    },
    setColoredClass: function(item){
        var coloredClass = item.attr("rel");
        $.cookie("coloredClass",coloredClass, { path: "/" });
        this._body.addClass(coloredClass);
    },
    cleanColoredClass: function() {
        var _this = this;
        _this._items.parent().each(function() {
            _this._body.removeClass('colored_' + $(this).attr('class'));
        });
    },
    isSelected: function(li){
        return li.hasClass(this._selectedClass);
    },
    addSelected: function(li){
        li.addClass(this._selectedClass);
    },
    removeSelected: function(){
        this._items.parent().removeClass(this._selectedClass);
    }

});