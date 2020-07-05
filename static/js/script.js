$(document).ready(function() {
    $('.routeButton').on('click',function(event) {
        $("#accordion").html("");
        var async1 = $.ajax({            
            data: {
                origin : $('#origin').val(),
                destination : $('#destination').val()
            },
            type: 'POST',
            url: '/routes',
            //contentType: "application/json; charset=utf-8",
            //dataType: "json",
            success: function( data ){    
			},
			error: function(error){
			}
        });

        var async2 = $.ajax({           
            data: {
                origin : $('#origin').val(),
                destination : $('#destination').val()
            },
            type: 'GET',
            url: '/route_time_dist',
            success: function(data) {
            },
            error: function(data) {
            }            
        });
        $.when(async2, async1).done(function(result2, result1) {
            json = JSON.parse(result2[0])
            console.log(json.rows[0]['elements'][0]['distance'].text)
            console.log(json.rows[0]['elements'][0]['duration'].text)
            console.log(json.rows[0]['elements'][0]['fare'].currency)
            console.log(json.rows[0]['elements'][0]['fare'].text)
            
            data = result1[0];

            // $.each(json.rows.person, function(i, v) {
            //     if (v.name == "Peter") {
            //         alert(v.age);
            //         return;
            //     }
            // });

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
                    "<p class=\"font-weight-bold\">" + json.rows[0]['elements'][0]['distance'].text + "  " + json.rows[0]['elements'][0]['duration'].text + "  " + json.rows[0]['elements'][0]['fare'].text + "</p>"+
                    "<a class=\"btn btn-link collapsed\" data-toggle=\"collapse\" data-target=\"#collapse"+ i +"\" aria-expanded=\"false\" aria-controls=\"collapse"+ data[i]+"\">"+                      
                    "<i class=\"fa fa-chevron-down\" aria-hidden=\"true\"></i></a></div></div></h5></div>"+
                    "<div id=\"collapse"+ i+"\" class=\"collapse\" aria-labelledby=\"heading"+ i+"\" data-parent=\"#accordion\">"+
                    "<div class=\"card-body\"><div class=\"progress\">"+
                    "<div class=\"progress-bar progress-bar-striped bg-success\" role=\"progressbar\" style=\"width: 25%\" aria-valuenow=\"25\" aria-valuemin=\"0\" aria-valuemax=\"100\"></div></div>" 
                    + data[i].FROM + " -" + viaName + data[i].TO  + "</div></div></div>"));
            }           
        });
        event.preventDefault();
    });
});


// .done(function() {
//     console.log('done');
// });