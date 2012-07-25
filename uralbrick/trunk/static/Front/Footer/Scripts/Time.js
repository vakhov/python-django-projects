var Time = Base.extend({
    constructor: function(){
        this._hours = $(".footer_time_hours");
        this._minutes = $(".footer_time_minutes");
        this._time = $(".footer_time");
        this.run();
    },
    run: function(){
        var _this = this;
        setInterval(function(){
            _this.updateTime();
        },1000);
    },
    updateTime: function(){
        var date = new Date();
        this._hours.text(this.leadingZero(date.getHours()));
        this._minutes.text(this.leadingZero(date.getMinutes()));
        this._time.toggleClass("footer_time__even");
    },
    leadingZero: function(num){
        return num < 10 ? "0" + num : num;
    }
});