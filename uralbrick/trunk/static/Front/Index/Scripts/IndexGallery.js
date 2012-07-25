var IndexGallery = Base.extend({
    constructor: function() {
        this._container = $(".index_gallery");
        this._gallery = $(".index_gallery_list");
        this._pics = $(".illustrations li");
        
        //this._gallery.empty();

        // $.getJSON('/json/', function(data) {
        //     json = new Array();
        //     json = data;

        //     for (var i = 0; i < data.length; i++) {
        //         $('.illustrations').append('<li id="illustration_' + i + '><img src="media/' + data[i].big_sharp_picture + '" alt="" /><ins></ins></li>');
        //         $('.index_gallery_list').append('<li class="index_gallery_item index_gallery_item__selected" rel="illustration_' + i + '"><span class="title"><a href="#">' + i + 'Кирпич</a></span><span class="text colored_bgColor">Супер Кирпич<br/><a href="#" class="blackLink">Кирпич</a></span></li>')
        //     };
        // });


        // $.getJSON('/json/', function(data) {
        //     json = new Array();
        //     json = data

        //     // for (var i = 0; i < json.length; i++) {
        //     //     $('.illustrations').append('<li id="illustration_' + i '"><img src="' + i['big_sharp_picture'] + '" alt="" /><ins></ins></li>')
        //     // };

        //     for (var i = 0; i < json.length; i++) {
        //         $('.illustrations').append('<li id="illustration_' + i '"><img src="' + i['big_sharp_picture'] + '" alt="" /><ins></ins></li>')
        //         $('.index_gallery_list').append('<li class="index_gallery_item index_gallery_item__selected" rel="illustration_1"><span class="title"><a href="#">' + i + 'Кирпич</a></span><span class="text colored_bgColor">Супер Кирпич<br/><a href="#" class="blackLink">Кирпич</a></span></li>')
        //     };
            

        // });


        this.updateItems();
        this._itemsCount = this._items.length;
        if ($("body").hasClass(IndexGallery.enabledClass)) {
            this.loadInit();
        }
    },
    loadInit: function() {
        var _this = this;
        $(window).load(function() {
            _this._pics.each(function() {
                $(this).css({
                    visibility: "visible",
                    display: "none"
                });
            });
            _this._container.css({ visibility: "visible" });
            _this.updateSelectedPic();
            _this.updateHeight();
            _this.register();
        });
        $(window).resize(function() {
            _this.updateHeight();
        });
    },
    register: function() {
        var number = this.getSelectedNumber();
        var _this = this;
        this._gallery.jcarousel({
            scroll: 1,
            start: number,
            buttonNextHTML: "<div><span></span></div>",
            buttonPrevHTML: "<div><span></span></div>",
            itemFallbackDimension: 750,
            wrap: "circular",
            itemFirstInCallback: {
                onBeforeAnimation: function(arg, selected, index, state){
                    if (state != "init") {
                        selected = $(selected);
                        _this.updateIllustration(state, selected);
                        _this.updateFooterGallery(state);
                        $(".footer_gallery .jcarousel-"+state).trigger("click");
                    }
                }
            }
        });
    },
    updateItems: function() {
        this._items = this._gallery.find(".index_gallery_item");
    },
    updateSelectedPic: function() {
        var oldSelected = this._pics.filter("." + IndexGallery.selectedPicClass);
        var newSelected = $("#" + this.getSelected().attr("rel"));
        if (oldSelected.length != 0)
            oldSelected
                .removeClass(IndexGallery.selectedPicClass)
                .hide();//("slow");
        newSelected
            .addClass(IndexGallery.selectedPicClass)
            .show();//.fadeIn("slow");
        $(".illustrations li img").attr('src', '#');
        this.applySrcFromPresrc(newSelected);
        this.applySrcFromPresrc(newSelected.prev());
        this.applySrcFromPresrc(newSelected.next());
    },
    applySrcFromPresrc: function(item) {
        var presrc = item.find('img').attr('presrc');
        item.find('img').attr('src', presrc);        
    },
    updateIllustration: function(direction, item) {
        this.updateItems();
        var selected = this.getSelected();
        if (item.length != 0) {
            selected.removeClass(IndexGallery.selectedClass);
            item.addClass(IndexGallery.selectedClass);
            this.updateSelectedPic();
        }
    },
    updateFooterGallery: function(direction) {
        var selected = $("." + FooterGallery.selectedClass);
        var item = direction == "prev" ? selected.prev() : selected.next();
        if (item.length != 0) {
            selected.removeClass(FooterGallery.selectedClass);
            item.addClass(FooterGallery.selectedClass);
        }

    },
    updateHeight: function() {
        var height = $(window).height() - 248;
        height = height < 200 ? 200 : height;
        this._container.css({ height: height });
    },
    getSelected: function() {
        return this._items.filter("." + IndexGallery.selectedClass);
    },
    getSelectedNumber: function() {
        var counter = 0;
        var number = 1;
        this._items.each(function() {
            counter++;
            if ($(this).hasClass(IndexGallery.selectedClass))
                number = counter;
        });
        return number;
    }
}, {
    selectedClass: "index_gallery_item__selected",
    selectedPicClass: "illustrations_item__selected",
    enabledClass: "index_gallery_enabled"
});