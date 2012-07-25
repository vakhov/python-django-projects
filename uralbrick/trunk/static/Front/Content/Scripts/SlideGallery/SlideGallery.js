var SlideGallery = Base.extend({
    constructor: function(gallery, id){
        this._gallery = gallery;
        this._galleryId = id;
        this._viewPort = this._gallery.find("."+SlideGalleryConstants.viewPort);
        this._items = this._gallery.find("."+SlideGalleryConstants.item);
        this._next = this._gallery.find("."+SlideGalleryConstants.next);
        this._prev = this._gallery.find("."+SlideGalleryConstants.prev);
        this._iconsList = this._gallery.find("."+SlideGalleryConstants.iconsList);
        this._icons = null;
    },
    showItem: function(i){
        var item = $("#"+this._galleryId+"_"+i);
        var height = item.find("img").attr("height");
        item.addClass(SlideGalleryConstants.currentItemClass);
        item.fadeIn();
        this._viewPort.animate({height:height},300);
    },
    hideItem: function(i){
        var item = $("#"+this._galleryId+"_"+i);
        item.removeClass(SlideGalleryConstants.currentItemClass);
        item.hide();
    },
    setCurrentIcon: function(i){
        var icon = $("#"+this._galleryId+"_"+i+"_icon");
        icon.addClass(SlideGalleryConstants.currentIconClass);
    },
    unsetCurrentIcon: function(i){
        var icon = $("#"+this._galleryId+"_"+i+"_icon");
        icon.removeClass(SlideGalleryConstants.currentIconClass);
    },
    setIdFor: function(items,i,id){
        $(items.get(i)).attr("id",id);
    },
    createIcons: function(html){
        this._icons = $(html);
        this._icons.appendTo(this._iconsList);
    },
    setItemSizes: function(items, i, sizes){
        var image = $(items.get(i)).find("img");
        image.attr("width",sizes.width).attr("height",sizes.height);
    },
    getItemSizes: function(items, i){
        var image = $(items.get(i)).find("img");
        var width = image.width();
        var height = image.height();
        return {width:width, height:height};
    },
    getId: function(){
        return this._galleryId;
    },
    getItems: function(){
        return this._items;
    },
    getIcons: function(){
        return this._icons;
    },
    getNext: function(){
        return this._next;
    },
    getPrev: function(){
        return this._prev;
    },
    getItemId: function(items,i){
        return $(items.get(i)).attr("id");
    },
    getLength: function(){
        return this._items.length;
    }
},{});