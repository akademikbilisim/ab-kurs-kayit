function fnFormatDetails ( dTable, nTr )
{
    var aData = dTable.fnGetData( nTr );
    var sOut = '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">';
    sOut += '<tr><td><b>Ãnvan:</b></td><td>'+aData[7]+'</td></tr>';
    sOut += '<tr><td><b>Kurum:</b></td><td>'+aData[8]+'</td></tr>';
    sOut += '<tr><td><b>Ãniversite:</b></td><td>'+aData[9]+'</td></tr>';
    sOut += '<tr><td><b>BÃ¶lÃ¼m:</b></td><td>'+aData[10]+'</td></tr>';
    sOut += '<tr><td><b>Ek Bilgiler:</b></td><td>'+aData[11]+'</td></tr>';
    sOut += '<tr><td>Secilen Diger Kurslar: </td><td>'+aData[12]+'</td></tr>';
    sOut += '<tr><td></td><td>'+aData[13]+'</td></tr>';
    sOut += '</table>';
     
    return sOut;
}

$(document).ready(function(){
    $('[data-id="course_table"]').DataTable({
            "dom": 'Bfrtip',
            "language": {
                    "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Turkish.json"
            },
            "searching": false,
            "bJQueryUI": false,
            "ordering": true,
            "paging" : false,
            buttons : [
          'copyHtml5',
            'excelHtml5',
            'csvHtml5',
            'pdfHtml5'
                        ],
    });
    $('[data-id="course_table_control_panel"]').each(function(){
       var dTable = $(this).dataTable({
            "dom": 'Bfrtip',
            "language": {
              "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Turkish.json"
            },
            "columnDefs": [
               {
                "targets": [ 7 ],
                "visible": false
               },
               {
                "targets": [ 8 ],
                "visible": false
               },
               {
                "targets": [ 9 ],
                "visible": false
               },
               {
                "targets": [ 10 ],
                "visible": false
               },
               {
                "targets": [ 11 ],
                "visible": false
               },
               {
                "targets": [ 12 ],
                "visible": false
               },
               {
                "targets": [ 13 ],
                "visible": false
               }
            ],
            "searching": false,
            "bJQueryUI": false,
            "ordering": true,
            "paging" : false,
            buttons : [
              'copyHtml5',
              'excelHtml5',
              'csvHtml5',
              'pdfHtml5'
            ],
      });

      dTable.find('tbody a').click(function(){
             var nTr = $(this).parents('tr')[0];
          if ( dTable.fnIsOpen(nTr) )
          {
              dTable.fnClose( nTr );
         1 }
          else
          {
              dTable.fnOpen( nTr, fnFormatDetails(dTable, nTr), 'details' );
          }
      });

    });

	$('#course_table tbody tr').click(function(){
		var attr = 	$(this).attr('href');
		if (typeof attr !== typeof undefined && attr !== false) {
			window.location=attr;
		}
	});


  $("#sendPreference").click(function(){
    var selectedCourse = JSON.stringify($("#field-container-form").serializeArray());
	var jsonData = {};
	jsonData['course'] = selectedCourse;
	jsonData['csrfmiddlewaretoken'] = getCookie('csrftoken');
	console.log(JSON.stringify(jsonData));
		$.ajax({
		    url : "/egitim/applytocourse", 
		    type : "POST",
		    dataType: "json", 
		    data : jsonData,
		    success : function(json) {
				bootbox.alert(json.message, function() {});
		    },
		    error : function(xhr,errmsg,err) {
				bootbox.alert(errmsg, function() {});
		    }
		});
  });

  $("#cancel-all").click(function(){
    var selectedCourse = "BaÅvurduÄunuz Kurslar Ä°ptal Edilecektir</br></br>";
    $("#field-container-form select option:selected").each(function(){
        selectedCourse += "<strong>- " + $(this).text() + " </strong></br>";
    });
    jsonData = {};
	jsonData['csrfmiddlewaretoken'] = getCookie('csrftoken');
    bootbox.dialog({
        message: selectedCourse,
        title: "OnaylÄ±yor musunuz?",
        buttons: {
          success: {
            label: "Evet!",
            className: "btn-success",
            callback: function() {
		        $.ajax({
		            url : "/egitim/cancelallpreference/", 
		            type : "POST",
		            dataType: "json", 
		            data : jsonData,
		            success : function(json) {
		        		bootbox.alert(json.message, function() {});
                        location.reload();
		            },
		            error : function(xhr,errmsg,err) {
		        		bootbox.alert(errmsg, function() {});
                        location.reload();
		            }
		       });
            }
          },
          danger: {
            label: "HayÄ±r!",
            className: "btn-danger",
            callback: function() {
            }
          }
        }
   });
  });



  $('[data-id="applicationopen"]').change(function(){
    var isClosed = $(this).prop('checked');
    applyMessage = "<strong>" + $(this).parent().parent().find("strong").text() + "</strong></br>";
    if(isClosed){
      applyMessage += "Kursu BaÅvurulara AÃ§mak Ãzeresiniz";
    }else{
      applyMessage += "Kursu BaÅvurulara Kapatmak Ãzeresiniz";
    }
    jsonData = {};
    jsonData['isOpen'] = isClosed;
    jsonData['course'] = ($(this).attr("id")).split("-")[1];
	jsonData['csrfmiddlewaretoken'] = getCookie('csrftoken');
    bootbox.dialog({
        message: applyMessage,
        title: "OnaylÄ±yor musunuz?",
        buttons: {
          success: {
            label: "Evet!",
            className: "btn-success",
            callback: function() {
		        $.ajax({
		            url : "/egitim/cancelcourseapplication/", 
		            type : "POST",
		            dataType: "json", 
		            data : jsonData,
		            success : function(json) {
		        		bootbox.alert(json.message, function() {
                          location.reload();
                        });
		            },
		            error : function(xhr,errmsg,err) {
		        		bootbox.alert(json.message, function() {
                          location.reload();
                        });
		            }
		       });
            }
          },
          danger: {
            label: "HayÄ±r!",
            className: "btn-danger",
            callback: function() {
            }
          }
        }
   });
  });

});
