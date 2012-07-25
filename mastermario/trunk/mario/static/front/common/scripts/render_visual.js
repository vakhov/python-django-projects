var RenderVisual = Base.extend({
    render: function() {
        this.renderTables();
        this.renderCapitalText();
        this.renderLeftMenu();
    },
    renderTables: function() {
        this.renderColorTable();
        this.renderTextTable();
        this.renderSimpleTable();
    },
    renderColorTable: function() {
        var tables = $(".tableColored");
        tables.each(function() {
            var table = $(this);
            table
                .attr("cellspacing", "0")
                .attr("cellpadding", "0");
            if (table.find("th").length != 0) {
                table.find("th:first").parents("tr:first").find("th").addClass("firstRow");
                table.find("th:last-child").addClass("lastCol");
                var max_count = 0;
                table.find("tr").each(function() {
                    var count = $(this).find("th").length;
                    if (count > max_count) max_count = count;
                });
                table.find("tr").each(function() {
                    var count = $(this).find("th").length;
                    if (count < max_count) $(this).find(".lastCol").removeClass("lastCol");
                });
            }
            table.find("td:first").parents("tr:first").find("td").addClass("firstRow");
            table.find("td:last-child").addClass("lastCol");
            table.find("tr:odd td").addClass("even");
            table.find("tr").mouseenter(
                function() {
                    $(this).addClass("hover");
                }).mouseleave(function() {
                    $(this).removeClass("hover");
                });
        });
    },
    renderTextTable: function() {
        var tables = $(".tableText");
        tables.each(function() {
            var table = $(this);
            table.attr("cellspacing", "0").attr("cellpadding", "0");
            table.find("th:last-child").addClass("lastCol");
            table.find("td:last-child").addClass("lastCol");
            table.find("tr").mouseenter(
                function() {
                    $(this).addClass("hover");
                }).mouseleave(function() {
                    $(this).removeClass("hover");
                });
        });
    },
    renderSimpleTable: function() {
        var tables = $(".tableSimple");
        tables.each(function() {
            var table = $(this);
            table
                .attr("cellspacing", "0")
                .attr("cellpadding", "0");
            table.find("tr:last-child").addClass("lastRow");
            table.find("tr:even td").addClass("even");
        });
    },
    renderCapitalText: function() {
        var capital = $("p.capital");
        capital.each(function() {
            var cap_obj = $(this);
            var cap_text = cap_obj.text();
            var cap_letter = cap_text.charAt(0);
            var new_cap_text = cap_text.substr(1, cap_text.length - 1);
            cap_obj.text(new_cap_text);
            $('<ins class="r">' + cap_letter + '</ins>').prependTo(this);
        });
    },
    renderLeftMenu: function() {
        $(".leftMenu p a").click(function(){
            $(this).parents(".leftMenu_group").toggleClass("group_hide");
            return false;
        });
        $(".leftMenu_innerMenu").each(function() {
            var item = $(this);
            item.find(">a, >ins").click(function() {
                item.toggleClass("show");
                return false;
            });
        });
    }
});