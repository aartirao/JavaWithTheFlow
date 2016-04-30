var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
 };
 
$(function() {
    getUserId(getUrlParameter("username"));
});

function getUserId(username) {
    $.ajax({url: '/getUserId/'+username, success: function(result){
        displayRecommendations(username, result.result);
    } 
    });   
}

function displayRecommendations(username, userId) {
   var user = {"username" : username};
   $.ajax({url: '/getRecommendations/'+userId, success: function(result){
        $("#templates").load("/static/templates/recco.html", function() {
            var template = document.getElementById('reccotemplate').innerHTML;
            qList = result["data"];
            for(var i=0; i<qList.length; i++) {
                qList[i]["username"] = username;
                var output = Mustache.render(template, qList[i], user);
                $("#reccobar").append(output);
            }    
        });            
    }});  
}