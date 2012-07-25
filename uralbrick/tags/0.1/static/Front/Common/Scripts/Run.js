var Run = function() {
    var colored = new Colored($(".colored_menu a"));
    colored.init();

    $(".openGallery_link").colorbox({
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
}

$(document).ready(function() {
    Run();
});