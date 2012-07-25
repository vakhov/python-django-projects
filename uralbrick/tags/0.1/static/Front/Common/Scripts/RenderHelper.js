var RenderHelper = Base.extend({},{
    setColoredBorder: function(items){
        items.addClass("colored_border");
    },
    listItems: function(lists){
        lists.each(function(){
            var list = $(this);
            var count = 1;
            list.find(">li").each(function(){
                var item = $(this);
                var num = $("<span class='item_num colored_bgColor colored_text'>"+count+".</span>");
                num.prependTo(item);
                count++;
            });
        });
    },
    renderTable: function(tables){
        tables.each(function(){
            var table = $(this);
            table.attr('cellpadding','0').attr('cellspacing','0');
            table.find("tr:last-child td").css("border-bottom","0");
            table.find("tr td:last-child, tr th:last-child").css("border-right","0");
            table.find("tr").mouseenter(function(){
                $(this).addClass("hover");
            }).mouseleave(function(){
                $(this).removeClass("hover");
            });
        });
    }
});