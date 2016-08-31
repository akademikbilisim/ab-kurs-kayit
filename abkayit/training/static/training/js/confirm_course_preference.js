$(document).ready(function(){

  $("#confirm_course_record_button_id").click(function(){
    var courseRecordId = $("#course_record_id").val();
	var jsonData = {};
	jsonData['courseRecordId'] = courseRecordId;
	jsonData['csrfmiddlewaretoken'] = getCookie('csrftoken');
	$.ajax({
	    url : "/egitim/approve_course_preference/", 
	    type : "POST",
	    dataType: "json", 
	    data : jsonData,
	    success : function(json) {
			bootbox.alert(json.message, function() {
                location.reload();
            });
            
	    },
	    error : function(xhr,errmsg,err) {
			bootbox.alert(errmsg, function() {
                location.reload();
            });
	    }
	});
  });

});
