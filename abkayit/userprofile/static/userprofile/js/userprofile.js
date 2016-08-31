function addPreference(selectedPreference){
  var container = $("#field-row-container");
  var text = $("#field-row").text();
  var idn = container.find("[data-id='container']").size() + 1;
  var id = "tercih" + idn
  var body = $(text.format(id, idn));
  body.find("button[data-id='remove']").click(function () {
    $(this).parents("[data-id='container']").remove();
  });
  container.append(body);


  var accomodations={}
  var selectOptions = "";
  $.ajax({
         url : "/accounts/getaccomodations/stu/"+$("#id_gender").val(),
         type : "GET",
         dataType: "json",
         success : function(data) {
                   accomodations=data;
                   $.each(accomodations,function(key,value){
                     selectOptions += "<option value='" + key + "'>" + value + "</option>"
                   });
                   body.find('select').append(selectOptions);
                   if(selectedPreference){
                     body.find('select').val(selectedPreference);
                   }
                   $("#remove").show();
         },
  });
}
function countrychanged(selectbox){
    var country = $(selectbox).val();
    if (country == "TR"){
        $("#id_ykimlikno").parent().parent().find('span').hide();
        $("#id_tckimlikno").parent().parent().find('div').first().append("<span class='required'></span>");
    }else{
        $("#id_tckimlikno").parent().parent().find('span').hide();
        $("#id_ykimlikno").parent().parent().find('div').first().append("<span class='required'></span>");
    }
}
function genderchanged(){
    if($(".accomodations_pref_div select").length){
      $("#field-row-container").html("");
      bootbox.alert("Konaklama Tercihlerinizi Güncelleyiniz", function(){});
      addPreference();
     }
}
$(document).ready(function(){
    $("#id_tckimlikno").parent().parent().find('div').first().append("<span class='required'></span>");
});