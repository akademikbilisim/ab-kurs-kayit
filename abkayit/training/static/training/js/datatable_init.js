$(document).ready(function(){
        $('#list_table').DataTable({
            "dom": 'Bfrtip',
            "language": {
                    "url": "/static/base/Turkish.json"
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

});
