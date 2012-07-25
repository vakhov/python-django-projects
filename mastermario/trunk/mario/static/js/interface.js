$(document).ready(function() {

    var global_IE6 = false;
    if ($("#ie6").length != 0) var global_IE6 = true; else var global_IE6 = false;
    if (global_IE6 || $("#ie7").length != 0 || $("#ie8").length != 0 || $("#ie9").length != 0) var global_IE = true; else var global_IE = false;

    initMainFrame();
    initSimpleSubmenu();
    lastThis($(".simple_submenu"), "li");
    hoverParent(".tag", $(".simple_tag_list .tag a"));
    randomFontSize($(".simple_tag_list .tag"), 11, 16);
    initSlideContent("click", $(".simple_tag_list"), ".more a", ".more_tags", ".more");
    mf_last_margin();

    initOutsideLinks();
    capitalText($("p.capital"));
    initTextGallery($(".text_gallery"), global_IE);
    alertText($(".alert"));
    imageLeft($(".image_left"));
    initSimpleImages($(".simple_image"));
    initSimpleImages($(".just_image"));
    initAutoRemark();
    initColorHeighter($(".color_heighter"));
    initLists();
    initComment($(".is_comment"));
    initTableColored();
    initTableText();
    initTableSimple();

});