/**
 * Created by Wasiq Noor on 6/25/2017.
 */


$('.btn-primary').click(function (event) {
    event.preventDefault();
    $.ajax({
        url: '/signin',
        data: $('.form-signin').serialize(),
        type: 'POST',
        success: function (response) {
            window.location.href = 'dashboard';
            console.log(response);
        },
        error: function (error) {
            console.log(error);
        }
    });
});
