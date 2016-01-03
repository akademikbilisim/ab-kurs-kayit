$(document).ready(function(){
        $('#list_table').DataTable({
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

});
