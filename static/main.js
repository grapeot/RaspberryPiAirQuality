$(function() {
    $('#msg').hide();
    $.get('/api/v1/jobs').done(function(data) {
        if (data.status != 'success') {
            $('#msg').html('Status failed.')
            $('#msg').show()
            return;
        }
        for (var item in data.result) {
            $('#items').append('<li>' + item.toString() + '</li>');
        }
    });
});
