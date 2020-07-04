$(document).ready(function() {
    $('.routeButton').on('click',function(event) {
        $("#accordion").html("");
        $.ajax({            
            data: {
                origin : $('#origin').val(),
                destination : $('#destination').val()
            },
            type: 'POST',
            url: '/routes',
            //contentType: "application/json; charset=utf-8",
            //dataType: "json",
            success: function( data ){
                console.log(data);
                for (i = 0; i < data.length; i++) {
                    var viaName = data[i].VIA == 'NA' ? ' ' : data[i].VIA + ' - ' ;
                    //console.log(data[i].VIA) 
                    $("#accordion").prepend($(
                        "<div class=\"card\">"+
                        "<div class=\"card-header\" id=\"heading"+ i+"\">"+
                        "<h5 class=\"mb-0 text-left\">"+
                        "<div class=\"btn-toolbar justify-content-between\" role=\"toolbar\" aria-label=\"Toolbar with button groups\">"+
                        "<div role=\"group\" aria-label=\"First group\">"+
                        "<a href=\"#\" class=\"badge badge-dark\"><i class=\"fa fa-bus\" aria-hidden=\"true\"></i> "+ data[i].BUS_NUMBER_1 +"</a></div>"+
                        "<div class=\"btn-group\">"+
                        "<p class=\"font-weight-bold\">46 m</p>"+
                        "<a class=\"btn btn-link collapsed\" data-toggle=\"collapse\" data-target=\"#collapse"+ i +"\" aria-expanded=\"false\" aria-controls=\"collapse"+ data[i]+"\">"+                      
                        "<i class=\"fa fa-chevron-down\" aria-hidden=\"true\"></i></a></div></div></h5></div>"+
                        "<div id=\"collapse"+ i+"\" class=\"collapse\" aria-labelledby=\"heading"+ i+"\" data-parent=\"#accordion\">"+
                        "<div class=\"card-body\"><div class=\"progress\">"+
                        "<div class=\"progress-bar progress-bar-striped bg-success\" role=\"progressbar\" style=\"width: 25%\" aria-valuenow=\"25\" aria-valuemin=\"0\" aria-valuemax=\"100\"></div></div>" + data[i].FROM + " -" + viaName + data[i].TO  + "</div></div></div>"));
                }              
			},
			error: function(error){
				console.log(error);
			}
        });
        event.preventDefault();
    });
});


// .done(function() {
//     console.log('done');
// });