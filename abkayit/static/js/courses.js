$(document).ready(function(){

    $('[data-id="course_table"]').each(function(){
        $(this).DataTable({
             "language": {
                    "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Turkish.json"
             },
            "searching": true,
            "ordering": true,
            "paging" : false
        });
    });

	$('[data-id="course_table"]').click(function(){
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


});
