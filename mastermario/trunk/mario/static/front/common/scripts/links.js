var Links = Base.extend({
    render: function() {
        this.renderBlankLinks();
    },
    renderBlankLinks: function() {
        var blankLinks = $("a[target='_blank']");
        blankLinks.each(function() {
            $(this).addClass("blankLink");
            $(this).wrapInner("<span></span>");
            if ($(this).hasClass("blackLink")) $(this).addClass("blankLink__black");
            if ($(this).hasClass("redLink")) $(this).addClass("blankLink__red");
            if ($(this).hasClass("whiteLink")) $(this).addClass("blankLink__white");
        });
    }
});