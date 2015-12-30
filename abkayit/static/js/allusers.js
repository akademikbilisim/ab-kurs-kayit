$(document).ready(function(){
        $('#list_table').DataTable({
            "dom": 'T<"clear">lfrtip',
            "tableTools": {
                                "sSwfPath": "/static/images/copy_csv_xls_pdf.swf"
            },
            "language": {
                    "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Turkish.json"
            },
            "searching":false,
            "ordering": true,
            "paging" : false,
            buttons : [
                    'csv'
                ],
        });

});
