var Run = function() {
    var colored = new Colored($(".colored_menu a"));
    colored.init();

    $(".openGallery_link, .cBox").colorbox({
        maxWidth: '90%',
        maxHeight: '90%',
        rel:'openGallery'
    });

    var slideGalleryArea = new SlideGalleryArea();
    $(".slideGallery").each(function(){
        slideGalleryArea.registerGallery($(this));
    });

    // Render helper actions
    RenderHelper.setColoredBorder($("h2, h3, .tip, blockquote"));
    RenderHelper.listItems($(".content ul, .content ol"));
    RenderHelper.renderTable($(".content table"));
    RenderHelper.pseudoHover($(".catalogPosition_photo .photo"), $(".catalogPosition_photo"), "catalogPosition_photo__hover");
    RenderHelper.pseudoHover($(".catalogPosition_photo .zoom"), $(".catalogPosition_photo"), "catalogPosition_photo__hover");
    RenderHelper.sizeCloud($(".alphabet_result_cloud a"));

    $(".catalogList_item").each(function(){
        var photo = $(this).find(".photo a");
        var title = $(this).find("dt a");
        RenderHelper.pseudoHover(photo, $(this), "catalogList_item__hover");
        RenderHelper.pseudoHover(title, $(this), "catalogList_item__hover");
    });

    $(".catalogItem").each(function(){
        var photo = $(this).find(".photo a");
        var title = $(this).find("dt a");
        var price = $(this).find(".price span");
        RenderHelper.pseudoHover(photo, photo.parent(), "colored_border");
        RenderHelper.pseudoHover(title, photo.parent(), "colored_border");

        RenderHelper.pseudoHover(photo, $(this), "catalogItem__hover");
        RenderHelper.pseudoHover(title, $(this), "catalogItem__hover");

        RenderHelper.pseudoHover(photo, price, "colored_bgColor");
        RenderHelper.pseudoHover(title, price, "colored_bgColor");
    });

    $(".catalogItem__small").each(function(){
        var photo = $(this).find(".photo img");
        var title = $(this).find("dt a");
        var price = $(this).find(".price");
        RenderHelper.pseudoHover(photo, photo, "colored_border");
        RenderHelper.pseudoHover(title, photo, "colored_border");

        RenderHelper.pseudoHover(photo, $(this), "catalogItem__small_hover");
        RenderHelper.pseudoHover(title, $(this), "catalogItem__small_hover");

        RenderHelper.pseudoHover(photo, price, "colored_bgColor");
        RenderHelper.pseudoHover(title, price, "colored_bgColor");
    });

    var slideAllow = true;
    $(".catalogPosition_link__paramsShow").click(function(){
        var paramsVisible = $(".catalogPosition_params").css("display") == "block";
        var likeVisible = $(".catalogPosition_like").css("display") == "block";
        if (slideAllow) {
            if (!paramsVisible && likeVisible) {
                $(".catalogPosition_like").slideToggle({complete: function(){
                    $(".catalogPosition_params").slideToggle({complete: function(){ slideAllow = true; }});
                }});
            } else {
                $(".catalogPosition_params").slideToggle({complete: function(){ slideAllow = true; }});
            }
        }
        slideAllow = false;
        return false;
    });
    $(".catalogPosition_link__likeShow").click(function(){
        var paramsVisible = $(".catalogPosition_params").css("display") == "block";
        var likeVisible = $(".catalogPosition_like").css("display") == "block";
        if (slideAllow) {
            if (paramsVisible && !likeVisible) {
                $(".catalogPosition_params").slideToggle({complete: function(){
                    $(".catalogPosition_like").slideToggle({complete: function(){ slideAllow = true; }});
                }});
            } else {
                $(".catalogPosition_like").slideToggle({complete: function(){ slideAllow = true; }});
            }
        }
        slideAllow = false;
        return false;
    });

    var FilterLink = Base.extend({
        constructor: function(link, content){
            this._slideAllow = true;
            var _this = this;
            link.click(function(){
                if (_this._slideAllow) {
                    this._slideAllow = false;
                    content.slideToggle({
                        complete: function(){
                            _this._slideAllow = true;
                        }
                    });
                    link.parent().toggleClass("filter_list_item__selected");
                }
                return false;
            });
        }
    });
    new FilterLink($(".color_filter_link"),$(".color_filter"));
    new FilterLink($(".price_filter_link"),$(".price_filter"));
    new FilterLink($(".purpose_filter_link"),$(".purpose_filter"));

    var alphabetFilter = new AlphabetFilter();
    alphabetFilter.registerHandlers();

    var filters = new Filters();
    filters.registerHandlers();

    new FooterSearch();
    new Time();
    new FooterGallery();
    new IndexGallery();

    $(".submit").click(function(){
        $(this).parents("form").submit();
        return false;
    });

    // Window
    $(".window").click(function(event){
        event.stopPropagation();
    });

    $(".footer_question .close").click(function(){
        $(".service_menu__question a").click();
    });

    $(".service_menu__question a").click(function(){
        var li = $(this).parents("li");
        $(".footer_question").stop(true, true).fadeToggle("slow");
        li.toggleClass("selected");
        return false;
    });

    $(".header_phone_call").click(function(){
        $(".header_call").fadeToggle("slow");
        return false;
    });

    $(".header_call .close").click(function(){
        $(".header_phone_call").click();
    });


}

$(document).ready(function() {
    $("body").addClass("loading");
    Run();
    $("body").removeClass("loading");    
});