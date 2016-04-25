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
            
			
		})
		.fail(function () {
			//Handle the error
        });
		});