
$(document).ready(function() {
    $("#cancel-all").click(function () {
        var selectedCourse = "Başvurular İptal Edilecektir. Kabul edildiğiniz kursları iptal etmeniz durumunda profilinize bu bilgi kaydedilecektir.</br></br>";
        selectedCourse += "<label for=\"cancelnote\">Neden?</label><input type=\"text\" class=\"form-control\" id=\"cancelnote\"/>"
        var jsonData = {};
        jsonData['csrfmiddlewaretoken'] = getCookie('csrftoken');
        $.ajax({
            url: "/egitim/getpreferredcourses/",
            type: "POST",
            dataType: "json",
            data: jsonData,
            success: function (json) {
                if (json.status == "0") {
                    $.each(json.preferred_courses, function (index, course) {
                        selectedCourse += "<strong>- " + course + " </strong></br>";
                    });
                }
            },
            error: function (xhr, errmsg, err) {
                console.log(errmsg);
            },
            complete: function () {
                jsonData = {};
                jsonData['csrfmiddlewaretoken'] = getCookie('csrftoken');
                bootbox.dialog({
                    message: selectedCourse,
                    title: "Onaylıyor musunuz?",
                    buttons: {
                        success: {
                            label: "Evet!",
                            className: "btn-success",
                            callback: function () {
                                jsonData['cancelnote'] = $('#cancelnote').val();
                                $.ajax({
                                    url: "/egitim/cancelallpreference/",
                                    type: "POST",
                                    dataType: "json",
                                    data: jsonData,
                                    success: function (json) {
                                        bootbox.alert(json.message, function () {
                                        });
                                        location.reload();
                                    },
                                    error: function (xhr, errmsg, err) {
                                        bootbox.alert(errmsg, function () {
                                        });
                                        location.reload();
                                    }
                                });
                            }
                        },
                        danger: {
                            label: "Hayır!",
                            className: "btn-danger",
                            callback: function () {
                            }
                        }
                    }
                });

            }
        });
    });
})