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

function checkActive(username) {
	$.ajax({url: '/isactive/'+username, success: function(result){
        setVizLinks(result.result);
    } 
    });
}

$(function(){
    checkActive(getUrlParameter("username"));
});