function setVizLinks(active){
	if(active) {
		$("#vis1").hide();
		$("#vis2").show();
		$("#vis3").show();
	} else {
		$("#vis1").show();
		$("#vis2").hide();
		$("#vis3").hide();
	}
}

function getUrlParameter(sParam) {
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
}   

function checkActive(username) {
	$.ajax({url: '/isactive/'+username, success: function(result){
        setVizLinks(result.result);
    } 
    });
}

$(function(){
    checkActive(getUrlParameter("username"));
});