var Filters = Base.extend({
    constructor: function() {
        var self = this;
        this._containers = $(".price_filter, .color_filter, .purpose_filter");
        this._priceRange = new RangeInput($(".rangeInput"), 100, function() {
            self.renderResult($(".price_filter"));
        });
        this._colorFilterLinks = $(".color_filter_item a");
        this._proposeFilterLinks = $(".purpose_filter a");
    },
    registerHandlers: function() {
        var self = this;
        this._colorFilterLinks.mouseenter(
            function() {
                if ($(this).hasClass("selected")) $(this).addClass("remove");
            }).mouseleave(
            function() {
                if ($(this).hasClass("selected")) $(this).removeClass("remove");
            }).click(function() {
                $(this).toggleClass("selected").removeClass("remove");
                self.renderResult($(".color_filter"));
                return false;
            });
        this._proposeFilterLinks.click(function() {
            var input = $(this).find("input");
            $(this).toggleClass("checked");
            input.val($(this).hasClass("checked"));
            self.renderResult($(".purpose_filter"));
            return false;
        });
    },
    renderResult: function(renderContainer) {
        var data = this.collectData();
        var self = this;
        $.ajax({
            url: "get_count.php",
            type: "POST",
            dataType: "json",
            data: { data: $.toJSON(data) },
            success: function(count) {
                self.render(renderContainer, count);
            }
        });
    },
    render: function(container, count) {
        if (parseInt(count) > 0) {
            if (!container.hasClass("filter_container__changed")) {
                this._containers
                    .removeClass("filter_container__changed")
                    .removeClass("colored_border")
                    .find(".showMore")
                    .hide();
                container
                    .addClass("filter_container__changed")
                    .addClass("colored_border");
                container.find(".showMore").slideDown();
            }
            container.find(".showMore ins").text(count);
        } else {
            this._containers
                .removeClass("filter_container__changed")
                .removeClass("colored_border")
                .find(".showMore")
                .hide();
        }
    },
    collectData: function() {
        var price = this.getPriceData();
        var color = this.getColorData();
        var propose = this.getProposeData();
        return {price:price,color:color,propose:propose};
    },
    getPriceData: function() {
        var min = $(".price_filter .min").val();
        var max = $(".price_filter .max").val();
        return {min: min, max: max};
    },
    getColorData: function() {
        var colors = {};
        $(".color_filter a.selected").each(function() {
            colors[$(this).attr("name")] = $(this).attr("value");
        });
        return colors;
    },
    getProposeData: function() {
        var propose = {};
        $(".purpose_filter .checked input").each(function() {
            propose[$(this).attr("name")] = $(this).val();
        });
        return propose;
    }
});