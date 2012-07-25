var SlideGalleryControl = Base.extend({
    constructor: function(slideGallery){
        this._slideGallery = slideGallery;
        this._currentItem = 0;
        this.register();
    },
    register: function(){
        this.registerItems();
        this.registerIcons();
    },
    registerSizes: function(){
        var items = this._slideGallery.getItems();
        for (var i = 0; i < items.length; ++i) {
            var sizes = this._slideGallery.getItemSizes(items,i);
            this._slideGallery.setItemSizes(items,i,sizes);
        }
    },
    registerItems: function(){
        var items = this._slideGallery.getItems();
        var id = this._slideGallery.getId();
        for (var i = 0; i < items.length; ++i) {
            var itemId = id + "_" + (i+1);
            this._slideGallery.setIdFor(items,i,itemId);
        }
    },
    registerIcons: function(){
        var items = this._slideGallery.getItems();
        var iconsHtml = "";
        for (var i = 0; i < items.length; ++i) {
            var id = this._slideGallery.getItemId(items,i);
            iconsHtml += SlideGalleryConstants.getIconLayout(id);
        }
        this._slideGallery.createIcons(iconsHtml);
    },
    setCurrent: function(i){
        this._currentItem = i;
        this._slideGallery.showItem(i);
        this._slideGallery.setCurrentIcon(i);
    },
    unsetCurrent: function(i){
        this._slideGallery.hideItem(i);
        this._slideGallery.unsetCurrentIcon(i);
    },
    doNext: function(){
        var length = this._slideGallery.getLength();
        var i = this._currentItem + 1 > length ? 1 : this._currentItem + 1;
        this.doItem(i);
    },
    doPrev: function(){
        var length = this._slideGallery.getLength();
        var i = this._currentItem - 1 < 1 ? length : this._currentItem - 1;
        this.doItem(i);
    },
    clickIcon: function(icon){
        var galleryId = this._slideGallery.getId();
        var i = parseInt(icon.attr("id").replace(galleryId,"").replace("_icon","").replace("_",""));
        this.doItem(i);
    },
    doItem: function(i){
        this.unsetCurrent(this._currentItem);
        this.setCurrent(i);
        this._currentItem = i;
    },
    getIcons: function(){
        return this._slideGallery.getIcons();
    },
    getPrev: function(){
        return this._slideGallery.getPrev();
    },
    getNext: function(){
        return this._slideGallery.getNext();
    }
},{});