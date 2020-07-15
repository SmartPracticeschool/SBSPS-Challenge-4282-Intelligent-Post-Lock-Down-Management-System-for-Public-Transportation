$(document).ready(function() {
    $('.routeButton').on('click',function(event) {
        $("#accordion").html("");
        var async1 = $.ajax({            
            data: {
                origin : $('#originStop').val(),
                destination : $('#destinationStop').val()
            },
            type: 'GET',
            url: '/routes',
            success: function( data ){  
                console.log(data)
			},
			error: function(error){
			}
        });

        var async2 = $.ajax({           
            data: {
                origin : $('#originStop').val(),
                destination : $('#destinationStop').val()
            },
            type: 'GET',
            url: '/route_time_dist',
            success: function(data) {
                console.log(data)
            },
            error: function(data) {
            }            
        });

        var async3 = $.ajax({           
            data: {
                origin : $('#originStop').val(),                
                destination : $('#destinationStop').val()
            },
            type: 'GET',
            url: '/homedata',
            success: function(data) {
                console.log(data)
            },
            error: function(data) {
            }            
        });
        $.when(async3,async2, async1).done(function(result3,result2, result1) {
            json = JSON.parse(result2[0])
            console.log(json)
            data = result1[0];
            console.log(data)
            seat = result3[0];
            console.log(seat)

            for (i = 0; i < data.length; i++) {
                var viaName = data[i].VIA == 'NA' ? ' ' : data[i].VIA + ' - ' ;
                var fare = json.rows[0]['elements'][0].status ==  "ZERO_RESULTS" ? 0 : json.rows[0]['elements'][0]['fare'].text;
                var distance = json.rows[0]['elements'][0].status ==  "ZERO_RESULTS" ? 0 : json.rows[0]['elements'][0]['distance'].text;
                var duration = json.rows[0]['elements'][0].status ==  "ZERO_RESULTS" ? 0 : json.rows[0]['elements'][0]['duration'].text;
                $("#accordion").prepend($(
                    "<div class=\"card\">"+
                    "<div class=\"card-header\" id=\"heading"+ i+"\">"+
                    "<h5 class=\"mb-0 text-left\">"+
                    "<div class=\"btn-toolbar justify-content-between\" role=\"toolbar\" aria-label=\"Toolbar with button groups\">"+
                    "<div role=\"group\" aria-label=\"First group\">"+
                    "<a href=\"#\" class=\"badge badge-dark\"><i class=\"fa fa-bus\" aria-hidden=\"true\"></i> "+ data[i].BUS_NUMBER_1 +"</a></div>"+
                    "<div class=\"btn-group\">"+
                    "<p class=\"font-weight-bold\">"+ duration + "</p>"+
                    "<a class=\"btn btn-link collapsed\" data-toggle=\"collapse\" data-target=\"#collapse"+ i +"\" aria-expanded=\"false\" aria-controls=\"collapse"+ data[i]+"\">"+                      
                    "<i class=\"fa fa-chevron-down\" aria-hidden=\"true\"></i></a></div></div></h5></div>"+
                    "<div id=\"collapse"+ i+"\" class=\"collapse\" aria-labelledby=\"heading"+ i+"\" data-parent=\"#accordion\">"+
                    "<div class=\"card-body text-left\"><img src=\"/static/images/gps.png\"/> " 
                    + data[i].FROM + " -" + viaName + data[i].TO  + "<br> <img src=\"/static/images/road.png\"/> "  + distance + " <img src=\"/static/images/fare.png\"/> " 
                    +  fare + " <img src=\"/static/images/seat.png\"/> " + seat[0][0] +" <img src=\"/static/images/queue.png\"/> " + seat[0][1] + "</div></div></div>"));
            }           
        });
        event.preventDefault();
    });
});
