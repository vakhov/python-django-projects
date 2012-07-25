var RangeInput = Base.extend({
    constructor: function(range, step, onSlide) {
        this._range = range;
        this._min = this._range.find("input.min");
        this._max = this._range.find("input.max");
        this._line = this._range.find(".rangeInput_line");
        this._step = typeof step == "undefined" ? 1 : step;
        this._minTip = null;
        this._maxTip = null;
        this._slider = this.createRange();
        this._onSlide = onSlide;
    },
    createRange: function() {
        var _this = this;
        var defaultMin = parseInt(_this._min.attr("rel"));
        var defaultMax = parseInt(_this._max.attr("rel"));
        return this._line.slider({
            range: true,
            min: defaultMin,
            max: defaultMax,
            values: [ _this.getVal().min, _this.getVal().max ],
            step: _this._step,
            create: function(){
                $(".ui-slider-range").addClass("colored_bgColor");
                _this._minTip = $("<span class='rangeInput_tip rangeInput_tip__min'>"+_this.getVal().min+"</span>").appendTo($(".ui-slider-handle").get(0));
                _this._maxTip = $("<span class='rangeInput_tip rangeInput_tip__max'>"+_this.getVal().max+"</span>").appendTo($(".ui-slider-handle").get(1));
                _this.updateTipLeft();
            },
            stop: function(){
                _this._onSlide();
            },
            slide: function(event, ui) {
                _this.updateTipLeft();
                _this._minTip.text(ui.values[0]);
                _this._maxTip.text(ui.values[1]);
                _this._min.val(ui.values[0]);
                _this._max.val(ui.values[1]);
                _this._min.change();
                _this._max.change();
            }
        });
    },
    updateTipLeft: function(){
        this._minTip.css("left",this.calcLeft(this._minTip)+"px");
        this._maxTip.css("left",this.calcLeft(this._maxTip)+"px");
    },
    calcLeft: function(elm){
        return (-1)*(elm.width()+12-7)/2;
    },
    getVal: function() {
        var valueMin = this.filterVal(this._min);
        var valueMax = this.filterVal(this._max);
        return {min: valueMin, max: valueMax};
    },
    filterVal: function(field) {
        var defaultValue = parseInt(field.attr("rel"));
        var value = parseInt(field.val());
        return isNaN(value) || value < 1 ? defaultValue : value;
    }
});