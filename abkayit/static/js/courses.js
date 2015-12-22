$(document).ready(function(){
	$('#course_table').DataTable({
		 "language": {
				"url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Turkish.json"
         },
		"searching": true,
	    "ordering": true,
		"paging" : false
	});

	$('#course_table tbody tr').click(function(){
		var attr = 	$(this).attr('href');
		if (typeof attr !== typeof undefined && attr !== false) {
			window.location=attr;
		}
	});

	$('.selectable').click(function () {
	    var orderOneNotExists = $('.order-one.selected').size() === 0;
	    var orderTwoNotExists = $('.order-two.selected').size() === 0;
	    if ($(this).hasClass('selected')) {
	        $(this).parent().parent().find('button').removeClass('selected');
	        $(this).parent().parent().find('.selectable').find('i').removeClass('fa-thumbs-o-up');
	        $(this).parent().parent().find('.selectable').find('i').addClass('fa-thumbs-o-down');
	        if(!orderTwoNotExists){
	            	$('.order-two.selected').parent().parent().find('.order-one').addClass('selected');
	            	$('.order-two.selected').removeClass('selected');
	        }
	    } else {
	        if (orderOneNotExists) {
	            $(this).parent().parent().find('.order-one').addClass('selected');
	            $(this).addClass('selected');
	        	$(this).parent().parent().find('.selectable').find('i').removeClass('fa-thumbs-o-down');
	        	$(this).parent().parent().find('.selectable').find('i').addClass('fa-thumbs-o-up');
	        } else {
	            if (orderTwoNotExists) {
	                $(this).parent().parent().find('.order-two').addClass('selected');
	                $(this).addClass('selected');
	        		$(this).parent().parent().find('.selectable').find('i').removeClass('fa-thumbs-o-down');
	        		$(this).parent().parent().find('.selectable').find('i').addClass('fa-thumbs-o-up');
	            }
	        }
	    }
	});
	$('.order-one').click(function () {
	    var notSelected = $(this).parent().parent().find('.selected').size() === 0;
	    if (!notSelected) {
	        if (!$(this).hasClass('selected')) {
	            $('.order-one.selected').parent().find('.order-two').addClass('selected');
	            $('.order-one.selected').removeClass('selected');
	            $(this).addClass('selected');
	            $(this).parent().find('.order-two').removeClass('selected');
	        }
	    }
	});
	$('.order-two').click(function () {
	    var notSelected = $(this).parent().parent().find('.selected').size() === 0;
	    if (!notSelected) {
	        if (!$(this).hasClass('selected')) {
	            $('.order-two.selected').parent().find('.order-one').addClass('selected');
	            $('.order-two.selected').removeClass('selected');
	            $(this).addClass('selected');
	            $(this).parent().find('.order-one').removeClass('selected');
	        }
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


	$('.apply-to-course').on('click', function(){
		var jsonData = {};
		var item = [];
		var selectedItems = $("#course_table tbody tr th button i[class='fa fa-thumbs-o-up']");
		selectedItems.each(function(){
			var courseId = $(this).parent().attr('id').split('_')[1];
			var preference = 0;
			if ($("#button_"+courseId).parent().parent().find('.order-one.selected').size() ==1 ){
				preference = "1";
			}
			else if ($("#button_"+courseId).parent().parent().find('.order-two.selected').size() ==1 ){
				preference = "2";
			}
			
			item.push('{"id":"'+courseId+'", "preference": "'+preference+'"}')	
		});
		jsonData['course'] = "[" + item.join(',') + "]";
		jsonData['csrfmiddlewaretoken'] = getCookie('csrftoken');
		console.log(JSON.stringify(jsonData));
		$.ajax({
		    url : "/egitim/applytocourse", 
		    type : "POST",
		    dataType: "json", 
		    data : jsonData,
		    success : function(json) {
				alert(json.status);
		    },
		    error : function(xhr,errmsg,err) {
		        alert(xhr.status + ": " + xhr.responseText);
		    }
		});

	})
})

	;
