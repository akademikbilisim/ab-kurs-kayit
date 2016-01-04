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
    var selectedCourse = "Başvurduğunuz Kurslar İptal Edilecektir</br></br>";
    $("#field-container-form select option:selected").each(function(){
        selectedCourse += "<strong>- " + $(this).text() + " </strong></br>";
    });
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
  });

});
