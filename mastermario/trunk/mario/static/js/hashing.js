check_link_hashes = function() {
    var hashes = {}
    var hash_list = []
    $('a[hash-string]').each(function() {
        hash_string = $(this).attr('hash-string');
        hashes[hash_string] = $(this);
        hash_list.push(hash_string);
    });
    if (hash_list.length) {
        $.ajax({
            async: true,
            type: 'POST',
            url: '/api/hashing/links/',
            data: $.toJSON(hash_list),
            dataType: 'json',
            processData: false,
            success: function(data) {
                for (var i in data) {
                    hashes[i].attr('href', data[i]);
                    hashes[i].removeAttr('hash-string');
                }
            } 
        });
    }
}

check_widget_hashes = function() {
    var hashes = {}
    var hash_list = []
    $('.hashed-widget').each(function() {
        hash_string = $(this).attr('hash-string');
        hashes[hash_string] = $(this);
        hash_list.push(hash_string);
    });
    if (hash_list.length) {
        $.ajax({
            async: true,
            type: 'POST',
            url: '/api/hashing/widgets/',
            data: $.toJSON(hash_list),
            dataType: 'json',
            processData: false,
            success: function(data) {
                for (var i in data) {
                    hashes[i].replaceWith(data[i]);
                }
            } 
        });
    }
}

$(document).ready(function() {
    check_link_hashes();
    check_widget_hashes();
})