$(document).ready(function() {
    $('#logo_wrapper').css('cursor', 'pointer').click(function() {
        window.location.href = '/';
    });

    $('#catalog_typeselect').find('dt').find('span').click(function() {
        $(this).parent().next('dd').toggle();
        //$(this).parent().next('dd').show();
    })
})