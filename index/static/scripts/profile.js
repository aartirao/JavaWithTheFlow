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
    //Ajax to get the user details
    var userId = getParametersByName("uId");
    var cId = getParametersByName("cId");
    if (userId == cId) {
        $("#clickable").hide();
    }
    var url = "getUserDetails/" + userId;
    $.ajax(
        {
            url: url,
            beforeSend: function (xhr) {

            },
            error: function (xhr) {

            },
            type: "GET"
        })
        .done(function (data) {
            if (data.status == "successfully retrieved") {
                $("#name").html(data.data.UserData.DisplayName);
                $("#aboutme").html(data.data.UserData.AboutMe);
                $("#date").html(data.data.UserData.CreationDate);
                $("#hidden").html(data.data.UserData.UserId);

                var followingHtml = "";
                $.each(data.data.Followers, function (key, element) {
                    var hyperlink = "/profile?uId=" + element.UserId + "&cId=" + cId;
                       var htmlItem = "";
                    if (userId == cId) {
                       htmlItem = "<p class='link'><a id='link-" + element.UserId + "' class = 'followlink' href='" + hyperlink + "'>" + element.DisplayName + "</a>   <i class='fa fa-times unfollow' aria-hidden='true'></i></p>";
                    }
                    else{
                        htmlItem = "<p class='link'><a id='link-" + element.UserId + "' class = 'followlink' href='" + hyperlink + "'>" + element.DisplayName + "</a></p>";
                    }

                    followingHtml = followingHtml + htmlItem;

                });
                $("#followerlinks").html(followingHtml);

                var followerHtml = "";
                $.each(data.data.Following, function (key, element) {
                    //var cId = getParametersByName("cId");
                    var hyperlink = "/profile?uId=" + element.UserId + "&cId=" + cId;
                    var htmlItem = "<p class='link'><a id='link-" + element.UserId + "' class = 'followlink' href='" + hyperlink + "'>" + element.DisplayName + "</a></p>";
                    followerHtml = followerHtml + htmlItem;
                });
                $("#followinglinks").html(followerHtml);
            }
        })
        .fail(function () {
            //handle error 
        });

    $("#dialogOk").dialog({
        autoOpen: false,
        open: function (event, ui) { $(".ui-dialog-titlebar-close", ui.dialog | ui).hide(); },
        show: {
            effect: "blind",
            duration: 1000
        },
        hide: {
            effect: "explode",
            duration: 1000
        },
        buttons: {
            Ok: function () {
                $(this).dialog("close");
                //Redirect
            }
        }
    });

    $("#dialogOkFollow").dialog({
        autoOpen: false,
        open: function (event, ui) { $(".ui-dialog-titlebar-close", ui.dialog | ui).hide(); },
        show: {
            effect: "blind",
            duration: 1000
        },
        hide: {
            effect: "explode",
            duration: 1000
        },
        buttons: {
            Ok: function () {
                $(this).dialog("close");
                //Redirect
            }
        }
    });
/*
    $("#dialogUnfollow").dialog({
        autoOpen: false,
        open: function (event, ui) { $(".ui-dialog-titlebar-close", ui.dialog | ui).hide(); },
        show: {
            effect: "blind",
            duration: 1000
        },
        hide: {
            effect: "explode",
            duration: 1000
        },
        buttons: {
            Ok: function () {
                $(this).dialog("close");
                //Redirect
            },
            Cancel: function () {
                return;

            }
        }
    });*/


});

$(document).on("click", "i[class='fa fa-times unfollow']", function () {
    //$("#dialogUnfollow").dialog("open");

    var userId = getParametersByName("cId");

    var url = "unfollow";
    var href = $(this).parent().find("a").attr("href");
    
    var followId = getParametersByName("uId", href);
    var postData = {
        "UserId": userId,
        "Follow": followId
    };
    $.ajax(
        {
            url: url,
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
                //modal pop up
                //console.log("Hello man");
                $(this).closest('.link').remove();
                //$(this).parent().remove();
                //$(this).hide();
                //$(this).remove();
                $("#dialogOk").dialog("open");
            }

        })
        .fail(function () {
            //handle error
        });
});
$(document).on("click", "span[id='clickable']", function () {
    var url = "follow";
    var followId = getParametersByName("uId");
    var currentLoggedUserId = getParametersByName("cId");
    var postData = {
        "UserId": currentLoggedUserId,
        "Follow": followId
    };
    $.ajax(
        {
            url: url,
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
                //modal pop up
                $("#dialogOkFollow").dialog("open");

            }
        })
        .fail(function () {
            //handle error
        });
});