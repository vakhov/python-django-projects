(function(b) {
    b.fn.lightBox = function(a) {
        function o() {
            b("body").append('<div id="jquery-overlay"></div><div id="jquery-lightbox"><div id="lightbox-container-image-box"><div id="lightbox-container-image"><img id="lightbox-image"><div style="" id="lightbox-nav"><a href="#" id="lightbox-nav-btnPrev"></a><a href="#" id="lightbox-nav-btnNext"></a></div><div id="lightbox-loading"><a href="#" id="lightbox-loading-link"><img src="' + a.imageLoading + '"></a></div></div></div><div id="lightbox-container-image-data-box"><div id="lightbox-container-image-data"><div id="lightbox-image-details"><span id="lightbox-image-details-caption"></span><span id="lightbox-image-details-currentNumber"></span></div><div id="lightbox-secNav"><a href="#" id="lightbox-secNav-btnClose"><img src="' + a.imageBtnClose + '" /></a></div></div></div></div>');
            var c = j();
            b("#jquery-overlay").css({backgroundColor:a.overlayBgColor,opacity:a.overlayOpacity,width:c[0],height:c[1]}).fadeIn();
            var d = k();
            b("#jquery-lightbox").css({top:d[1] + c[3] / 10,left:d[0]}).show();
            b("#jquery-overlay,#jquery-lightbox").click(function() {
                i()
            });
            b("#lightbox-loading-link,#lightbox-secNav-btnClose").click(function() {
                i();
                return false
            });
            b(window).resize(function() {
                var e = j();
                b("#jquery-overlay").css({width:e[0],height:e[1]});
                var f = k();
                b("#jquery-lightbox").css({top:f[1] + e[3] / 10,left:f[0]})
            })
        }

        function g() {
            b("#lightbox-loading").show();
            a.fixedNavigation ? b("#lightbox-image,#lightbox-container-image-data-box,#lightbox-image-details-currentNumber").hide() : b("#lightbox-image,#lightbox-nav,#lightbox-nav-btnPrev,#lightbox-nav-btnNext,#lightbox-container-image-data-box,#lightbox-image-details-currentNumber").hide();
            var c = new Image;
            c.onload = function() {
                b("#lightbox-image").attr("src", a.imageArray[a.activeImage][0]);
                p(c.width, c.height);
                c.onload = function() {
                }
            };
            c.src = a.imageArray[a.activeImage][0]
        }

        function p(c, d) {
            var e = b("#lightbox-container-image-box").width(),f = b("#lightbox-container-image-box").height(),l = c + a.containerBorderSize * 2,m = d + a.containerBorderSize * 2;
            e = e - l;
            f = f - m;
            b("#lightbox-container-image-box").animate({width:l,height:m}, a.containerResizeSpeed, function() {
                q()
            });
            if (e == 0 && f == 0)b.browser.msie ? n(250) : n(100);
            b("#lightbox-container-image-data-box").css({width:c});
            b("#lightbox-nav-btnPrev,#lightbox-nav-btnNext").css({height:d + a.containerBorderSize * 2})
        }

        function q() {
            b("#lightbox-loading").hide();
            b("#lightbox-image").fadeIn(function() {
                b("#lightbox-container-image-data-box").slideDown("fast");
                b("#lightbox-image-details-caption").hide();
                a.imageArray[a.activeImage][1] && b("#lightbox-image-details-caption").html(a.imageArray[a.activeImage][1]).show();
                r()
            });
            if (a.imageArray.length - 1 > a.activeImage) {
                objNext = new Image;
                objNext.src = a.imageArray[a.activeImage + 1][0]
            }
            if (a.activeImage > 0) {
                objPrev = new Image;
                objPrev.src = a.imageArray[a.activeImage - 1][0]
            }
        }

        function r() {
            b("#lightbox-nav").show();
            b("#lightbox-nav-btnPrev,#lightbox-nav-btnNext").css({background:"transparent url(" + a.imageBlank + ") no-repeat"});
            if (a.activeImage != 0)a.fixedNavigation ? b("#lightbox-nav-btnPrev").css({background:"url(" + a.imageBtnPrev + ") left 15% no-repeat"}).unbind().bind("click", function() {
                a.activeImage -= 1;
                g();
                return false
            }) : b("#lightbox-nav-btnPrev").unbind().hover(
                function() {
                    b(this).css({background:"url(" + a.imageBtnPrev + ") left 15% no-repeat"})
                },
                function() {
                    b(this).css({background:"transparent url(" + a.imageBlank + ") no-repeat"})
                }).show().bind("click", function() {
                a.activeImage -= 1;
                g();
                return false
            });
            if (a.activeImage != a.imageArray.length - 1)a.fixedNavigation ? b("#lightbox-nav-btnNext").css({background:"url(" + a.imageBtnNext + ") right 15% no-repeat"}).unbind().bind("click", function() {
                a.activeImage += 1;
                g();
                return false
            }) : b("#lightbox-nav-btnNext").unbind().hover(
                function() {
                    b(this).css({background:"url(" + a.imageBtnNext + ") right 15% no-repeat"})
                },
                function() {
                    b(this).css({background:"transparent url(" + a.imageBlank + ") no-repeat"})
                }).show().bind("click", function() {
                a.activeImage += 1;
                g();
                return false
            });
            s()
        }

        function s() {
            b(document).keydown(function(c) {
                if (c == null) {
                    keycode = event.keyCode;
                    escapeKey = 27
                } else {
                    keycode = c.keyCode;
                    escapeKey = c.DOM_VK_ESCAPE
                }
                key = String.fromCharCode(keycode).toLowerCase();
                if (key == a.keyToClose || key == "x" || keycode == escapeKey)i();
                if (key == a.keyToPrev || keycode == 37)if (a.activeImage != 0) {
                    a.activeImage -= 1;
                    g();
                    b(document).unbind()
                }
                if (key == a.keyToNext || keycode == 39)if (a.activeImage != a.imageArray.length - 1) {
                    a.activeImage += 1;
                    g();
                    b(document).unbind()
                }
            })
        }

        function i() {
            b("#jquery-lightbox").remove();
            b("#jquery-overlay").fadeOut(function() {
                b("#jquery-overlay").remove()
            });
            b("embed, object, select").css({visibility:"visible"})
        }

        function j() {
            var c,d;
            if (window.innerHeight && window.scrollMaxY) {
                c = window.innerWidth + window.scrollMaxX;
                d = window.innerHeight + window.scrollMaxY
            } else if (document.body.scrollHeight > document.body.offsetHeight) {
                c = document.body.scrollWidth;
                d = document.body.scrollHeight
            } else {
                c = document.body.offsetWidth;
                d = document.body.offsetHeight
            }
            var e,f;
            if (self.innerHeight) {
                e = document.documentElement.clientWidth ? document.documentElement.clientWidth : self.innerWidth;
                f = self.innerHeight
            } else if (document.documentElement && document.documentElement.clientHeight) {
                e = document.documentElement.clientWidth;
                f = document.documentElement.clientHeight
            } else if (document.body) {
                e = document.body.clientWidth;
                f = document.body.clientHeight
            }
            pageHeight = d < f ? f : d;
            pageWidth = c < e ? c : e;
            return arrayPageSize = [pageWidth,pageHeight,e,f]
        }

        function k() {
            var c,d;
            if (self.pageYOffset) {
                d = self.pageYOffset;
                c = self.pageXOffset
            } else if (document.documentElement && document.documentElement.scrollTop) {
                d = document.documentElement.scrollTop;
                c = document.documentElement.scrollLeft
            } else if (document.body) {
                d = document.body.scrollTop;
                c = document.body.scrollLeft
            }
            return arrayPageScroll = [c,d]
        }

        function n(c) {
            var d = new Date;
            do var e = new Date; while (e - d < c)
        }

        a = jQuery.extend({overlayBgColor:"#000",overlayOpacity:0.8,fixedNavigation:false,imageLoading:"design/img/lightbox/lightbox-ico-loading.gif",imageBtnPrev:"design/img/lightbox/lightbox-btn-prev.gif", imageBtnNext:"design/img/lightbox/lightbox-btn-next.gif",imageBtnClose:"design/img/lightbox/lightbox-btn-close.gif",imageBlank:"design/img/lightbox/lightbox-blank.gif",containerBorderSize:10,containerResizeSpeed:400,txtImage:"\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435",txtOf:"\u0438\u0437",keyToClose:"c",keyToPrev:"p",keyToNext:"n",imageArray:[],activeImage:0}, a);
        var h = this;
        return this.unbind("click").click(function() {
            b("embed, object, select").css({visibility:"hidden"});
            o();
            a.imageArray.length = 0;
            a.activeImage = 0;
            if (h.length == 1)a.imageArray.push([this.getAttribute("href"),this.getAttribute("title")]); else for (var c = 0; c < h.length; c++)a.imageArray.push([h[c].getAttribute("href"),h[c].getAttribute("title")]);
            for (; a.imageArray[a.activeImage][0] != this.getAttribute("href");)a.activeImage++;
            g();
            return false
        })
    }
})(jQuery);