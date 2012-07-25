Aphaline = {}

require(

    ["api", "widgetlist", "toolbar", "editor", "actions", "legacy", "interface"], 
    
    function() {
        require.ready(function() {
            Aphaline.Interface.init();
        });
    }
    
);
