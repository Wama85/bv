//static/js/signUp.js
$(function() {
    $('#btnSignUp').click(function() {
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response); alert(response)
                $('#message').html(response);
                if(response == 'ok'){
                    window.location.href = '/login';
                }
            },
            error: function(error) {
                console.log(error);
                $('#message').html(error);
            }
        });
    });
});