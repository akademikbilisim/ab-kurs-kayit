function fnFormatDetails ( dTable, nTr )
{
    var aData = dTable.fnGetData( nTr );
    var sOut = '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">';
    sOut += '<tr><td><b>Ünvan:</b></td><td>'+aData[7]+'</td></tr>';
    sOut += '<tr><td><b>Kurum:</b></td><td>'+aData[8]+'</td></tr>';
    sOut += '<tr><td><b>Üniversite:</b></td><td>'+aData[9]+'</td></tr>';
    sOut += '<tr><td><b>Bölüm:</b></td><td>'+aData[10]+'</td></tr>';
    sOut += '<tr><td><b>Ek Bilgiler:</b></td><td>'+aData[11]+'</td></tr>';
    sOut += '<tr><td><b>Kursiyerin Seçtiği Diğer Kurslar: </b></td><td>'+aData[12]+'</td></tr>';
    sOut += '<tr><td></td><td>'+aData[13]+'</td></tr>';
    sOut += '</table>';
    sOut += '</br>';
    sOut += '<div class="score">';
    sOut += '<div class="form-group">';
    sOut += '<div class="row">';
    sOut += aData[14];
    sOut += '</div>';
    sOut += '</div>';
    sOut += '<div class="form-group">';
    sOut += '<div class="row">';
    sOut += aData[15];
    sOut += '</div>';
    sOut += '</div>';
    sOut += '<div class="form-group">';
    sOut += '<div class="row">';
    sOut += aData[16];
    sOut += '</div>';
    sOut += '</div>';
    sOut += '</div>';
     
    return sOut;
}

$(document).ready(function(){
    $('[data-id="course_table"]').DataTable({
            "dom": 'Bfrtip',
            "language": {
                    "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Turkish.json"
            },
            "searching": true,
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
               },
               {
                "targets": [ 14 ],
                "visible": false
               },
               {
                "targets": [ 15 ],
                "visible": false
               },
               {
                "targets": [ 16 ],
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
              console.log("detail is clicked")
              dTable.fnOpen( nTr, fnFormatDetails(dTable, nTr), 'details' );
              dTable.find("#save-score").click(function(){
                  var score = $(this).closest(".score").find("select").val();
                  var note = $(this).closest(".score").find("input[type='text']").val();
                  var trainess_username = $(this).closest(".score").find("input[class='input-username']").val();
	              var jsonData = {};
	              jsonData['score'] = score;
	              jsonData['note'] = note;
	              jsonData['trainess_username'] = trainess_username;
	              jsonData['csrfmiddlewaretoken'] = getCookie('csrftoken');
	              console.log(JSON.stringify(jsonData));
	              $.ajax({
	                  url : "/accounts/savenote", 
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
          }
      });

    });

	$('#course_table tbody tr').click(function(){
		var attr = 	$(this).attr('href');
		if (typeof attr !== typeof undefined && attr !== false) {
			window.location=attr;
		}
	});


  $("#field-container-form").find("#sendPreference").click(function(){
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

  $("#field-container-for-addition-form").find("#sendPreference").click(function(){
    var selectedCourse = JSON.stringify($("#field-container-for-addition-form").serializeArray());
	var jsonData = {};
	jsonData['course'] = selectedCourse;
	jsonData['csrfmiddlewaretoken'] = getCookie('csrftoken');
	console.log(JSON.stringify(jsonData));
		$.ajax({
		    url : "/egitim/additionprefapply/", 
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
    var selectedCourse = "Başvurduğunuz Kurslar İptal Edilecektir</br></br>";
	
    var jsonData = {};
	jsonData['csrfmiddlewaretoken'] = getCookie('csrftoken');
	$.ajax({
	    url : "/egitim/getpreferredcourses/", 
	    type : "POST",
	    dataType: "json", 
	    data : jsonData,
	    success : function(json) {
            if(json.status == "0"){
                $.each( json.preferred_courses, function( index, course ){
                    selectedCourse += "<strong>- " + course + " </strong></br>";
                }); 
            }
	    },
	    error : function(xhr,errmsg,err) {
			console.log(errmsg);
	    },
        complete : function(){
            jsonData = {};
            jsonData['csrfmiddlewaretoken'] = getCookie('csrftoken');
            bootbox.dialog({
                message: selectedCourse,
                title: "Onaylıyor musunuz?",
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
                    label: "Hayır!",
                    className: "btn-danger",
                    callback: function() {
                    }
                  }
                }
           });

        }
	});
  });



/******************************************************/
/* #52 numarali issue ile kapatildi   

  $('[data-id="applicationopen"]').change(function(){
    var isClosed = $(this).prop('checked');
    applyMessage = "<strong>" + $(this).parent().parent().find("strong").text() + "</strong></br>";
    if(isClosed){
      applyMessage += "Kursu Başvurulara Açmak Üzeresiniz";
    }else{
      applyMessage += "Kursu Başvurulara Kapatmak Üzeresiniz";
    }
    jsonData = {};
    jsonData['isOpen'] = isClosed;
    jsonData['course'] = ($(this).attr("id")).split("-")[1];
	jsonData['csrfmiddlewaretoken'] = getCookie('csrftoken');
    bootbox.dialog({
        message: applyMessage,
        title: "Onaylıyor musunuz?",
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
            label: "Hayır!",
            className: "btn-danger",
            callback: function() {
            }
          }
        }
   });
  });
*/
});
