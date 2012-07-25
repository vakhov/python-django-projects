var AlphabetFilter = Base.extend({
    constructor: function(){
        this._links = $(".alphabet_filter a");
        this._renderContainer = $(".alphabet_result_container");
        this._renderBlock = $(".alphabet_result");
    },
    registerHandlers: function(){
        var self = this;
        this._links.click(function(){
            var link = $(this);
            self.removeSelected();
            self.addSelected(link);
            var symbol = self.getSymbol(link);
            self.hideResult(function(){
                self.sendSymbol(symbol);
            });
            return false;
        });
    },
    hideResult: function(complete){
        this._renderContainer.slideUp({
            complete: complete
        });
    },
    renderResult: function(html){
        this._renderBlock.html(html);
        this._renderContainer.slideDown();
    },
    sendSymbol: function(symbol){
        var self = this;
        $.ajax({
            url: "get_symbol.php",
            type: "POST",
            dataType: "json",
            data: { symbol: $.toJSON(symbol) },
            success: function(data){
                self.renderResult(data);
            }
        });
    },
    getSymbol: function(link){
        return link.text();
    },
    removeSelected: function(){
        this._links.removeClass("selected");
    },
    addSelected: function(link){
        link.addClass("selected");
    }
});