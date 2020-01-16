$(function(){
    $('.favolite-btn').on('click', function(event){
        event.preventDefault();
        $(this).toggleClass('active');

        if($(this).hasClass('active')){
        	$('.favolite-off').hide();
        	$('.favolite-on').show();
        } else {
        	$('.favolite-off').show();
        	$('.favolite-on').hide();
        }
    });
});