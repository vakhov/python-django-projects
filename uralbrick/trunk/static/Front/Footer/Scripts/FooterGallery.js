var FooterGallery = Base.extend({
    constructor: function(){
        this._container = $(".footer_gallery");
        this._gallery = this._container.find(".footer_gallery_list");
        this._items = this._gallery.find(".footer_gallery_item");
        if ($("body").hasClass(FooterGallery.enabledClass))
            this.register();
    },
    register: function(){
        var _this = this;
        var wrap = $("body").hasClass(IndexGallery.enabledClass) ? "circular" : null;
        this._gallery.jcarousel({
            scroll: 1,
            start: _this.getSelectedNumber(),
            itemFallbackDimension: 180,
            wrap: wrap
        });
        this.registerItems();
        $(".service_menu__power").click(function(){
            $(this).toggleClass("selected");
            _this._container.stop(false, true).slideToggle({ easing: "easeOutQuart", duration: 800 });
        });
    },
    registerItems: function(){
        this._items.each(function(){
            var item = $(this);
            // Delaying
            var deferred = function(item) { return function() {
                var img = item.find("img");
                if (img.width() || !img.attr('src')) {
                    clearInterval(item.data('deferred_interval'));
                }
                var left = (item.width() - img.width())/2;
                var border = item.find("."+FooterGallery.borderClass);
                var fade = item.find("."+FooterGallery.fadeClass);
                fade.css({
                    left: left,
                    width: img.width(),
                    height: img.height()
                });
                border.css({
                    left: left,
                    width: img.width() - 6,
                    height: img.height() - 6
                });
            }} (item);
            item.data('deferred_interval', setInterval(deferred, 100));
        }).click(function(){
            if (!$(this).hasClass(FooterGallery.selectedClass))
                window.location = $(this).find("a").attr("href");
        });
    },
    getSelectedNumber: function(){
        var counter = 0;
        var number = 1;
        this._items.each(function(){
            counter++;
            if ($(this).hasClass(FooterGallery.selectedClass))
                number = counter;
        });
        return number - 2;
    }
},{
    selectedClass: "footer_gallery_item__selected",
    borderClass: "footer_gallery_item_border",
    fadeClass: "footer_gallery_item_fade",
    enabledClass: "footer_gallery_enabled"
});