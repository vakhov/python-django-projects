var SlideGalleryConstants = Base.extend({},{
    viewPort: "slideGallery_viewPort",
    item: "slideGallery_item",
    next: "slideGallery_next",
    prev: "slideGallery_prev",
    iconsList: "slideGallery_icons",
    currentItemClass: "slideGallery_item__current",
    currentIconClass: "colored_bgColor",
    getIconLayout: function(id){
        return '<a href="#" id="'+id+'_icon" rel="'+id+'">&nbsp;</a>';
    }
});