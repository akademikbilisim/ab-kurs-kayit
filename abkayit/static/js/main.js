$(document).ready(function () {
    $("table input[type='checkbox']").change(function (e) {
        if ($(this).is(":checked")) {
            $(this).closest('tr').addClass("checked-trainee-course");
        } else {
            $(this).closest('tr').removeClass("checked-trainee-course");
        }
        if($(this).parent().parent().parent().find(".checked-for-another-course").length){
            $(this).closest('tr').addClass("checked-trainee-for-another-course");
        }
    });
    $("table input[type='checkbox']").trigger("change");
    $("table .checked-trainee-course").each(function(){
            $(this).closest('tr').attr("class","");
            $(this).closest('tr').addClass("checked-trainee-course");
    });
    $("table .approved-trainess-for-this-course").each(function(){
            $(this).closest('tr').attr("class","");
            $(this).closest('tr').addClass("approved-trainess-for-this-course");
    });
    $("table .checked-for-another-course").each(function(){
            $(this).closest('tr').attr("class","");
            $(this).closest('tr').addClass("checked-trainee-for-another-course");
    });
});




function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

String.prototype.format = function () {
    var str = this;
    for (var i = 0; i < arguments.length; i++) {
        var reg = new RegExp("\\{" + i + "\\}", "gm");
        str = str.replace(reg, arguments[i]);
    }
    return str;
};

function guid() {
    function s4() {
        return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
    }
    return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
        s4() + '-' + s4() + s4() + s4();
}
