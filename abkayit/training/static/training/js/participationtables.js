$(document).ready(function(){
    $('[data-id="course_table"]').DataTable({
            "dom": 'Bfrtip',
            "language": {
                    "url": "/static/base/Turkish.json"
            },
            "searching": false,
            "bJQueryUI": false,
            "ordering": false,
            "paging" : false,
    });
    $('#course_table tbody tr').click(function(){
		var attr = 	$(this).attr('href');
		if (typeof attr !== typeof undefined && attr !== false) {
			window.location=attr;
		}
	});
});
