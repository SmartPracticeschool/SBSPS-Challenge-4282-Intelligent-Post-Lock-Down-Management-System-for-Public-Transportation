$(document).ready(function() {
    setInterval(function() {
        $.ajax({
            type: "GET",
            url: "/adminsdata",
        }).done(function( data ) {
            var tableBusStopHtml = '';
            var tableBusHtml = '';
            bus_stop = data[0]
            bus = data[1]
            for (i = 0; i < bus_stop.length; i++) {
                tableBusStopHtml += '<tr>';
                row = bus_stop[i]
                for (j = 0 ; j < row.length; j++) {
                    tableBusStopHtml += '<td>'+row[j]+'</td>'
                }
                tableBusStopHtml += '</tr>';
            }
            $("#table-bus-stop").html("");
            $("#table-bus-stop").html(tableBusStopHtml)

            for (i = 0; i < bus.length; i++) {
                tableBusHtml += '<tr>';
                row = bus[i]
                for (j = 0 ; j < row.length; j++) {
                    tableBusHtml += '<td>'+row[j]+'</td>'
                }
                
                tableBusHtml += '<td>NA</td></tr>';
            }
            $("#table-bus").html("");
            $("#table-bus").html(tableBusHtml)

            }).fail(function(jqXHR, textStatus, errorThrown) {
                console.log(jqXHR, textStatus, errorThrown);
                });
    }, 100 * 60),

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