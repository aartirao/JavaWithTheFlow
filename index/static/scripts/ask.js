//JS used in ask.html
var CKEDITOR_BASEPATH = '/static/scripts/vendor/ckeditor/';
var username = "";
function getParametersByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)", "i"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

$(document).ready(function () {
    username = getParametersByName("username");
    var textreceived = getParametersByName("text");
    var tagreceived = getParametersByName("tags");

    if (textreceived != undefined) {
        $("#question-title").val(textreceived);

    }
    if (tagreceived != undefined) {
        $("#question-tags").val(tagreceived);
    }
    CKEDITOR.replace('richtext-area');
    
    $( "#dialog" ).dialog({
      autoOpen: false,
      open: function(event, ui) { $(".ui-dialog-titlebar-close", ui.dialog | ui).hide(); },
      show: {
        effect: "blind",
        duration: 1000
      },
      hide: {
        effect: "explode",
        duration: 1000
      },
      buttons: {
        Ok: function() {
          $( this ).dialog( "close" );
          //Redirect
        }
      }
    });
});

$(document).on("click", "button[class='post-question btn btn-primary']", function () {
    var textEntered = $("#question-title").val();
    var tagsEntered = $("#question-tags").val();

    var questionHtmlText = CKEDITOR.instances['richtext-area'].getData();
    if (textEntered.trim() == '') {
         $("#body-validate").text("");
        $("#title-validate").text("Title should not be empty");
        return;
    }
    if (questionHtmlText.trim() == '') {
        $("#title-validate").text("");
        $("#body-validate").text("Body should not be empty");
        return;
    }
    
    postData = {
        "Body": questionHtmlText,
        "Title": textEntered,
        "Tags": tagsEntered,
        "DisplayName": username
    };
    $.ajax(
        {
            url: "addQuestion",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(postData),
            beforeSend: function (xhr) {

            },
            error: function (xhr) {

            },
            type: "POST"

        })
        .done(function (data) {
            if (data.status == "successfully saved") {
               $( "#dialog" ).dialog( "open" );
            }
        })
        .fail(function () {

        });
});