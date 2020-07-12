$(document).ready(function() {
    $('#btnAnnnouncement').on('click',function(event) {
        $.ajax({            
            data: {
                post : $('#textareaPost').val(),
                link : $('#inputLink').val(),
                type : $('#inputType').val(),
                sentiment : $('#inputSentiment').val()
            },
            type: 'POST',
            url: '/announcements',
            //contentType: "application/json; charset=utf-8",
            //dataType: "json",
            success: function( data ){ 
                console.log(data)
                alert('Annoucemnet published successfully')   
			},
			error: function(error){
                alert('Annoucemnet publish falied.')  
			}
        });
        event.preventDefault();
    });
});


// .done(function() {
//     console.log('done');
// });