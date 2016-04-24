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


$(document).ready(function () {
	
	var url = "getViews";
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
            
            
			//var TopicTitle = json.topicName;
           	//	 var TopicViewCount= json.viewCount;
		//	console.log(TopicViewCount)
            
			var i=1;
            
			$.each(json, function (key, dataList) {
               // console.log(dataList.viewCount)
			//$(".cell-1").css("background-color","yellow");
              
			if(dataList.viewCount < 200000){
                
				$(".cell-"+i).text(dataList.topicName);
				$(".cell-"+i).css("background-color","#CCFFCC");
                i++;
			}
			else if(dataList.viewCount < 300000){
				$(".cell-"+i).text(dataList.topicName);
				$(".cell-"+i).css("background-color","#99ff99"); 
				i++;
			}
			else if(dataList.viewCount < 600000){
				$(".cell-"+i).text(dataList.topicName);;
				$(".cell-"+i).css("background-color","#66ff66"); 
                i++;
			}
			else if(dataList.viewCount < 900000){
					$(".cell-"+i).text(dataList.topicName);
					$(".cell-"+i).css({"background-color":"#00b21e","color":"white"});  
                    i++;
			}
			else if(dataList.viewCount < 1100000){
				$(".cell-"+i).text(dataList.topicName);
				$(".cell-"+i).css({"background-color":"#00A000","color":"white"});  
                i++;
			}
			else if(dataList.viewCount < 1400000){
				$(".cell-"+i).text(dataList.topicName);
				$(".cell-"+i).css({"background-color":"#009000","color":"white"});  
                i++;
			}
			else if(dataList.viewCount < 1600000){
				$(".cell-"+i).text(dataList.topicName);
				$(".cell-"+i).css({"background-color":"#008000","color":"white"}); 
                i++;
			}
			else if(dataList.viewCount < 1900000){
				$(".cell-"+i).text(dataList.topicName);
				$(".cell-"+i).css({"background-color":"#007000","color":"white"});
                i++; 
			}else if(dataList.viewCount < 2100000){
				$(".cell-"+i).text(dataList.topicName);
				$(".cell-"+i).css({"background-color":"#006000","color":"white"});
                i++;
			}else if(dataList.viewCount < 2400000){
				$(".cell-"+i).text(dataList.topicName);
				$(".cell-"+i).css({"background-color":"#005000","color":"white"});
                i++;
			}
			else if(dataList.viewCount < 2800000){
				$(".cell-"+i).text(dataList.topicName);
				$(".cell-"+i).css({"background-color":"#004000","color":"white"});
                i++;
			}
			else if(dataList.viewCount < 4800000){
				$(".cell-"+i).text(dataList.topicName);
				$(".cell-"+i).css({"background-color":"#003000","color":"white"});
                i++;
				}
			else if(dataList.viewCount < 6800000){
				$(".cell-"+i).text(dataList.topicName);				
				$(".cell-"+i).css({"background-color":"#002600","color":"white"})
		
                i++;
			}
			});
			
           
			
		//	$("#userdetail").html("by <a href='" + json.question.askedUserProfile + "'>" + json.question.askedbyUserName + "</a>");
		//	$("#askedtime").html("<span class='glyphicon glyphicon-time'></span> " + json.question.askedDate);
		//	$("#qtext").html(json.question.postText);
			
		})
		.fail(function () {
			//Handle the error
        });
		});