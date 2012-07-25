var FooterSearch = Base.extend({
    constructor: function(){
        this._field = $(".footer_search_text");
        this._watermark = $(".footer_search_watermark");
        this.registerHandlers();
    },
    registerHandlers: function(){
        var _this = this;
        this._field.blur(function(){
            if (_this.isEmpty()) {
                _this._watermark.show();
            }
        }).focus(function(){
            _this._watermark.hide();
        });
        this._watermark.click(function(){
            _this._field.focus();
        });
    },
    isEmpty: function(){
        return this._field.val() == "";
    }
});