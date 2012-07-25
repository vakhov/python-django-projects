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
        var firstClass = this._body.attr("class");
        this._items.each(function(){
            if ($(this).attr("rel") == firstClass)
                _this.addSelected($(this).parent());
            _this.registerHandlers($(this));
        });
    },
    registerHandlers: function(item){
        var li = item.parent();
        var _this = this;
        item.click(function(){
            if (!_this.isSelected(li)) {
                _this.removeSelected();
                _this.addSelected(li);
                _this.setColoredClass(item);
            }
            return false;
        });
    },
    setColoredClass: function(item){
        var coloredClass = item.attr("rel");
        $.cookie("coloredClass",coloredClass);
        this._body.attr("class",coloredClass);
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