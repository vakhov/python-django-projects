var RenderHelper = Base.extend({},{
    doubleClearing: function(parent, tag){
        parent.find(tag+":odd").next().addClass("clear");
    }
});