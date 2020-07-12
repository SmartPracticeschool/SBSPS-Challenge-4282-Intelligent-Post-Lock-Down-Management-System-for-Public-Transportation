$(document).ready(function() {
    $( window ).on( "load",function(event) {
        $("#news_cols").html("");
        $.ajax({
            type: 'GET',
            url: '/news_api',
            success: function( data ){
                console.log(data);
                for (i = 0; i < data.length; i++) {
                    $("#news_cols").prepend($(
                        "<div class=\"card\">"+
                        "<img class=\"card-img-top\" src=\"...\" alt=\"Card image cap\">"+
                        "<div class=\"card-body\">"+
                        "<h5 class=\"card-title\">" + data.articles[i].title + "</h5>"+
                        "<p class=\"card-text\">" + data.articles[i].description + "</p>"+
                        "<p class=\"card-text\"><small class=\"text-muted\">Last updated 3 mins ago</small></p>"+
                        "</div></div>" ));
                }
            },
            error: function(error){
            }
        }); 
        event.preventDefault();     
    });    
});
    
    
    // .done(function() {
    //     console.log('done');
    // });