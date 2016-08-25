function fnFormatDetails ( dTable, nTr )
{
    var aData = dTable.fnGetData( nTr );
    var sOut = '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">';
    sOut += '<tr><td><b>Ünvan:</b></td><td>'+aData[10]+'</td></tr>';
    sOut += '<tr><td><b>Üniversite:</b></td><td>'+aData[11]+'</td></tr>';
    sOut += '<tr><td><b>Bölüm:</b></td><td>'+aData[12]+'</td></tr>';
    sOut += '<tr><td><b>Ek Bilgiler:</b></td><td>'+aData[13]+'</td></tr>';
    sOut += '<tr><td><b>Kursiyerin Seçtiği Diğer Kurslar: </b></td><td>'+aData[14]+'</td></tr>';
    sOut += '<tr><td>Onaylandı mı?</td><td>'+aData[15]+'</td></tr>';
    sOut += '<tr><td></td><td>'+aData[16]+'</td></tr>';

    sOut += '</table>';
    sOut += '</br>';
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
               },
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
          }
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


  $("#cancel-all").click(function(){
    var selectedCourse = "Başvurular İptal Edilecektir. Kabul edildiğiniz kursları iptal etmeniz durumunda profilinize bu bilgi kaydedilecektir.</br></br>";
    selectedCourse += "<label for=\"cancelnote\">Neden?</label><input type=\"text\" class=\"form-control\" id=\"cancelnote\"/>"
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
                        jsonData['cancelnote'] = $('#cancelnote').val();
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
});
