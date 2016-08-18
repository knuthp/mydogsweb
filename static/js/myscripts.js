$(function() {
    $('button').click(function() {
        var day = $('#day').val();
        $.ajax({
            url: 'api/dogcam/images/' + day,
            contentType: "application/json; charset=utf-8",
            type: 'DELETE',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});