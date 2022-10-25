$(document).ready(function(){
    console.log('hola mundo');

    function ajax_login(){
        $.ajax({
            url: '/login-ajax',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                console.log(response);
            },
            error: function(response){
                console.log(response);
            }
        });
    }

    $("#login-form").submit(function(e){
        e.preventDefault();
        ajax_login();
    })

})