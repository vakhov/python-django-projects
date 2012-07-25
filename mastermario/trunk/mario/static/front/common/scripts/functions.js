var initMainFrame = function() {
    $(".mainframe tr td.mf_col:first-child").addClass("mf_first");
    $($(".mf_col h2").get(0)).css("margin-top", "0");
    $(".colors_blocks li span a").wrap('<table cellspacing="0" cellpadding="0"><tr><td></td></tr></table/>');
    $(".mf_col h2:first-child").addClass("first");
}
var initSimpleSubmenu = function() {
    $(".simple_submenu li.cur").prev().addClass("no_border");
    $(".simple_submenu").prev().css("margin-bottom", "0");
}
var hoverThis = function(obj) {
    if (obj.attr("id") != "") var name = obj.attr("id"); else var name = obj.attr("class");
    obj.mouseenter(
        function() {
            $(this).addClass("hover").addClass(name + "_hover");
        }).mouseleave(function() {
        $(this).removeClass("hover").removeClass(name + "_hover");
    })
}
var hoverParent = function(parent_obj, hover_obj) {
    hover_obj.each(function() {
        var tmp = $(this).parents(parent_obj);
        $(this).mouseenter(
            function() {
                $(this).parents(parent_obj).addClass("hover");
            }).mouseleave(function() {
            $(this).parents(parent_obj).removeClass("hover");
        });
    });
}
var closeButton = function(close_obj) {
    close_obj.find(".close").click(function() {
        close_obj.hide();
        return false;
    });
}
var lastThis = function(parent_obj, target_obj) {
    parent_obj.find(target_obj + ":last-child").addClass("last");
    parent_obj.find(target_obj + ":last").addClass("last");
}
var initTip = function(bind_type, tip_body, tip_objs, margin_x, margin_y) {
    var timeout = 0;
    if (tip_body.find(".close").length != 0) var is_close = true; else var is_close = false;
    tip_objs.bind(bind_type,
        function() {
            clearTimeout(timeout);
            tip_body
                .css("left", ($(this).offset().left - $("#site").offset().left + margin_x) + "px")
                .css("top", ($(this).offset().top - $("#site").offset().top + margin_y) + "px").show(200);
            if (tip_body.hasClass("arp_icon")) {
                tip_body.css("left", ($(this).offset().left - $("#site").offset().left + margin_x + $(this).width() - 7) + "px");
            }
        }).mouseleave(function() {
            if (!is_close) timeout = setTimeout(function() {
                tip_body.hide();
            }, 100);
        });
    if (bind_type != "click") tip_objs.click(function() {
        return false;
    });
    tip_body.mouseenter(
        function() {
            clearTimeout(timeout);
        }).mouseleave(function() {
            if (!is_close) timeout = setTimeout(function() {
                tip_body.hide();
            }, 100);
        });
}
var randomFontSize = function(obj, from, to) {
    var old_size = 16;
    obj.each(function() {
        var new_size = old_size;
        while (new_size == old_size) {
            new_size = Math.floor(Math.random() * (to - from + 1)) + from;
        }
        $(this).css("font-size", new_size + "px");
        old_size = new_size;
    });
}
var mf_last_margin = function() {
    $(".mainframe .mf_col").each(function() {
        var childs = $(this).find("h2");
        $(childs[childs.length - 1]).css("margin-bottom", 0);
    });
}
var initSlideContent = function(bind_type, parent_obj, slide_button, slide_content, class_obj) {
    parent_obj.find(slide_button).bind(bind_type, function() {
        parent_obj.find(slide_content).slideToggle(0);
        parent_obj.find(class_obj).toggleClass("slide_button_show");
        return false;
    });
}
var initOutsideLinks = function() {
    $(".simple_outside_links li.cur ins").each(function() {
        var ins = $(this);
        var span = ins.next();
        var li = ins.parent();
        ins.animate({width:(span.width() + 10)}, 1000, "", function() {
            li.addClass("selected");
        });
    });
}
var initTextGallery = function(tg_objs, global_IE) {
    tg_objs.each(function() {
        var tg_obj = $(this);
        var tg_counter = 0;
        var lis = tg_obj.find("li");
        var big_pic = tg_obj.find(".overflow");
        var li_first = tg_obj.find("li:first-child");

        var nextPoint = function(li) {
            lis.removeClass("cur");
            li.addClass("cur");

            if (big_pic.find("img").length != 0) {
                var img = big_pic.find("img");
                var old_height = img.height();
            }
            big_pic.html(li.find("span").html());
            var img = big_pic.find("img");
            var new_height = img.height();
            img.hide();
            big_pic
                .css("height", old_height + "px")
                .animate({
                    height:new_height
                }, 500, "", function() {
                    img.fadeIn(500);
                });
            tg_obj.find(".panel a").attr("href", li.find("a").attr("rel"));
            big_pic.find("img").click(function() {
                if (li.next().length != 0) var next_li = li.next(); else var next_li = li_first;
                nextPoint(next_li);
                return false;
            });
        }
        nextPoint(li_first);
        lis.find("a").click(function() {
            var a = $(this);
            var ul = a.parents("ul");
            var li = a.parents("li");
            if (!li.hasClass("cur")) {
                nextPoint(li);
            }
            return false;
        });
    });
}
var alertText = function(text) {
    text.each(function() {
        $('<span class="alert_text">важно</span>').prependTo(this);
    });
}
var imageLeft = function(text) {
    text.each(function() {
        $('<div class="clear"></div>').appendTo(this);
    });
}
var initSimpleImages = function(images) {
    images.each(function() {
        var image_obj = $(this).find("img");
        image_obj.wrap('<table cellspacing="0" cellpadding="0"><tr><td></td></tr></table>');
    });
}
var initColorHeighter = function(chs) {
    chs.each(function() {
        var ch_obj = $(this).find("a");
        ch_obj.wrap('<table cellspacing="0" cellpadding="0"><tr><td style="height:' + $(this).height() + 'px;"></td></tr></table>');
    });
}
var initAutoRemark = function() {
    initTip("click", $(".arp_cont"), $(".auto_remark"), -1, 27);
    initTip("mouseenter", $(".arp_icon"), $(".auto_remark"), 0, -11);
}
var initLists = function() {
    $("ul.number_marker").each(function() {
        var lis = $(this).find("li");
        var count = 0;
        lis.each(function() {
            count++;
            $("<ins>" + count + ".</ins>").prependTo(this);
        });
    });
}
var getCommentFrameHTML = function(id) {
    return '<div class="panel"><div class="panel_relative"><div class="panel_rep"><p class="view_comments"><a href="#">18 комментариев</a></p><p class="add_comment"><a href="#">добавить</a></p><p class="like"><a href="#">мне нравиться</a></p></div><div class="stripe"></div></div><div class="panel_top"><div class="png"></div></div><div class="panel_bottom"><div class="png"></div></div></div>';
}
var hideAllComments = function() {
    $(".is_comment .panel").hide();
}
var initComment = function(comments_obj) {
    comments_obj.each(function() {
        var comment_obj = $(this);
        var comment_id = comment_obj.attr("id");
        var frame_html = getCommentFrameHTML(comment_id);
        var is_animate = false;
        var timeout = 0;

        $(frame_html).appendTo(this);
        var comment_border = comment_obj.find(".border");
        var comment_panel = comment_obj.find(".panel");

        comment_obj.mouseenter(
            function() {
                clearTimeout(timeout);
                if (!is_animate) {
                    hideAllComments();
                    is_animate = true;
                    comment_panel.animate({width:159,right:-170}, 200, "",
                        function() {
                            is_animate = false;
                        }).show();
                }
            }).mouseleave(function() {
                if (!is_animate) {
                    timeout = setTimeout(function() {
                        is_animate = true;
                        comment_panel.animate({width:0,right:-8}, 200, "",
                            function() {
                                is_animate = false;
                            }).hide();
                    }, 100);
                }
            });

    });
}
