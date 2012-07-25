var WindowControl = Base.extend({
    constructor: function(){
        this._window = $(window);
        this._body = $('body');
    },
    getWidth: function(){
        return this._window.width();
    },
    getHeight: function(){
        return this._window.height();
    },
    getScrollTop: function(){
        return this._window.scrollTop();
    },
    getScrollLeft: function(){
        return this._window.scrollLeft();
    },
    setScrollTop: function(value){
        this._window.scrollTop(value);
    },
    setScrollLeft: function(){
        this._window.scrollLeft(value);
    },
    addScrollHandler: function(scrollHandler){
        this._window.scroll(function(){ scrollHandler(); });
    },
    addResizeHandler: function(resizeHandler){
        this._window.resize(function(){ resizeHandler(); });
    },
    addClickHandler: function(clickHandler){
        this._body.click(function(){ clickHandler(); });
    }
});