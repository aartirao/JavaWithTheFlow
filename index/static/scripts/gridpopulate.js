defaults = {
    callback: function () { }
	, decimal: false
	, disable: false
	, disableOpacity: 0.5
	, hideRange: false
	, klass: ''
	, min: 0
	, max: 10
	, start: 5
	, step: null
	, vertical: false
};

function getParametersByName(name, url) {
	if (!url) url = window.location.href;
	name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)", "i"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    console.log(results[2].replace(/\+/g, " "));
    return decodeURIComponent(results[2].replace(/\+/g, " "));

}

$(document).ready(function () {
	jQuery.ajaxSetup({
          beforeSend: function() {
             $('#loader').show();
          },
          complete: function(){
             $('#loader').hide();
          },
          success: function() {}
        });
	
	var url = "getViewCount";
	//Ajax call to get all the details about the question
	$.ajax(
		{
			url: url,
			beforeSend: function (xhr) {

			},
			error: function (xhr) {

			},
			method: "GET"
			
		})
		.done(function (data) {
			var json = data.data;
			console.log(json)
            
			var i=1
			var topicName = "";            
			$.each(json, function (key, dataList) {
               // console.log(dataList.viewCount)
			//$(".cell-1").css("background-color","yellow");

			$(".cell-"+i).click(function() {
				console.log(this.id);
			    window.location.href = '/questionList?topic='+this.id+'&username='+getParametersByName("username");
			});  

			if(dataList.viewCount < 200000){
				$(".cell-"+i).css("background-color","#CCFFCC");
			}
			else if(dataList.viewCount < 300000){
				$(".cell-"+i).css("background-color","#99ff99"); 
			}
			else if(dataList.viewCount < 600000){
				$(".cell-"+i).css("background-color","#66ff66"); 
			}
			else if(dataList.viewCount < 900000){
					$(".cell-"+i).css({"background-color":"#00b21e","color":"white"});  
			}
			else if(dataList.viewCount < 1100000){
				$(".cell-"+i).css({"background-color":"#00A000","color":"white"});  
			}
			else if(dataList.viewCount < 1400000){
				$(".cell-"+i).css({"background-color":"#009000","color":"white"});  
			}
			else if(dataList.viewCount < 1600000){
				$(".cell-"+i).css({"background-color":"#008000","color":"white"}); 
			}
			else if(dataList.viewCount < 1900000){
				$(".cell-"+i).css({"background-color":"#007000","color":"white"}); 
			}
			else if(dataList.viewCount < 2100000){
				$(".cell-"+i).css({"background-color":"#006000","color":"white"});
			}
			else if(dataList.viewCount < 2400000){
				$(".cell-"+i).css({"background-color":"#005000","color":"white"});
			}
			else if(dataList.viewCount < 2800000){
				$(".cell-"+i).css({"background-color":"#004000","color":"white"});
			}
			else if(dataList.viewCount < 4800000){
				$(".cell-"+i).css({"background-color":"#003000","color":"white"});    
			}
			else if(dataList.viewCount < 6800000){			
				$(".cell-"+i).css({"background-color":"#002600","color":"white"})
			}
				$(".cell-"+i).text(dataList.topicName);
				$(".cell-"+i).attr("id",dataList.topicName);
				i++;
			});
		
           
			
		//	$("#userdetail").html("by <a href='" + json.question.askedUserProfile + "'>" + json.question.askedbyUserName + "</a>");
		//	$("#askedtime").html("<span class='glyphicon glyphicon-time'></span> " + json.question.askedDate);
		//	$("#qtext").html(json.question.postText);
			
		})
		.fail(function () {
			//Handle the error
        });
		});