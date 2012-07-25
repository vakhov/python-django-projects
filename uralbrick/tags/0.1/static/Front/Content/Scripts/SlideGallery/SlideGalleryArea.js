var SlideGalleryArea = Base.extend({
    galleryCount: 0,
    registerGallery: function(gallery){
        this.galleryCount++;
        var id = "gallery_" + this.galleryCount;
        var galleryControl = new SlideGalleryControl(new SlideGallery(gallery, id));
        var prev = galleryControl.getPrev();
        var prevBg = prev.find(".slideGallery_navigation_bg");
        var next = galleryControl.getNext();
        var nextBg = next.find(".slideGallery_navigation_bg");
        $(window).load(function(){
            galleryControl.registerSizes();
            galleryControl.setCurrent(1);
        });
        var icons = galleryControl.getIcons();
        icons.click(function(){
            galleryControl.clickIcon($(this));
            return false;
        });
        prev.mouseenter(function(){
            prevBg.addClass("colored_border");
        }).mouseleave(function(){
            prevBg.removeClass("colored_border");
        }).click(function(){
            galleryControl.doPrev();
            return false;
        });
        next.mouseenter(function(){
            nextBg.addClass("colored_border");
        }).mouseleave(function(){
            nextBg.removeClass("colored_border");
        }).click(function(){
            galleryControl.doNext();
            return false;
        });
    }
},{});