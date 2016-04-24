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


var answerArray = [];
var CKEDITOR_BASEPATH = '/static/scripts/vendor/ckeditor/';

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
	var questionId = getParametersByName("qId");
	var url = "getQuestion";
	url = url + "/" + questionId;
	//Ajax call to get all the details about the question
	$.ajax(
		{
			url: url,
			beforeSend: function (xhr) {

			},
			error: function (xhr) {

			},
			method: "GET"
			//data: { qId : questionId }
		})
		.done(function (data) {
			var json = data.data;
			console.log(json)
			$("#qTitle").html(json.question.postTitle);
			$("#userdetail").html("by <a href='" + json.question.askedUserProfile + "'>" + json.question.askedbyUserName + "</a>");
			$("#askedtime").html("<span class='glyphicon glyphicon-time'></span> " + json.question.askedDate);
			$("#qtext").html(json.question.postText);
			var commentHtml = "";
			$.each(json.comments, function (key, comment) {
				var cHtml = "<p class='comment-p'>";
				cHtml = cHtml + comment.commentText;
				cHtml = cHtml + " - <a href='" + comment.userUrl + "'>" + comment.commentedUser + "</a>";
				cHtml = cHtml + " " + comment.commentedTime + "</p>";
				commentHtml = commentHtml + cHtml;
			});
			commentHtml = commentHtml + "<p class='add-comment-link'>add a comment</p>"
			$("#questioncomments").html(commentHtml);


			$("#answercontainer .answerheader h3").text(json.question.noOfAnswers + " Answers");
			$.each(json.answers, function (key, answeritem) {
				var answerobj = {
					answerid: "",
					answervoteid: "",
					answercontent: "",
					answertime: "",
					ansusername: "",
					answercommentdivid: "",
					answercomments: "",
					userUrl: "",
					usefulnesscount: "",
					upvoteid: "",
					downvoteid: ""
				};

				answerobj.answerid = "answer-" + answeritem.answer.postId;
				answerobj.answervoteid = "answervote-" + answeritem.answer.postId;
				answerobj.answercontent = answeritem.answer.postText;
				answerobj.answertime = answeritem.answer.answeredDate;
				answerobj.ansusername = answeritem.answer.answeredbyUserName;
				answerobj.answercommentdivid = "answer-comments-" + answeritem.answer.postId;
				answerobj.userUrl = answeritem.answer.answeredUserProfile;
				answerobj.usefulnesscount = answeritem.answer.upvotes;
				answerobj.upvoteid = "answerupvote-" + answeritem.answer.postId;
				answerobj.downvoteid = "answerdownvote-" + answeritem.answer.postId;

				var answercommentHtml = "";

				$.each(answeritem.comments, function (ckey, comment) {
					var cHtml = "<p class='comment-p'>";
					cHtml = cHtml + comment.commentText;
					cHtml = cHtml + " - <a href='" + comment.userUrl + "'>" + comment.commentedUser + "</a>";
					cHtml = cHtml + " " + comment.commentedTime + "</p>";
					answercommentHtml = answercommentHtml + cHtml;
				});

				answerobj.answercomments = answercommentHtml;
				answerArray.push(answerobj);

			});
			$("#answercontentcontainer").loadTemplate("/static/templates/answers.html", answerArray);
		})
		.fail(function () {
			//Handle the error

		});
		
		//Adding richtext editor
		CKEDITOR.replace('richtext-area');
});

$(document).on("click", "p[class='add-comment-link']", function () {
	var parent = $(this).parent();
	var newCommentHtml = "<div class = 'new-comment-element'>\
							<textarea rows='4' cols='50' class='newcomment-txtarea'></textarea>\
							<p><button class='submit btn btn-primary'>Save</button><button class='cancel btn btn-primary'>Cancel</button></p>\
						 </div>";
	parent.find(".new-comment-element").remove();
	//voteElement = parent.find(".voters")
	//$(newCommentHtml).insertBefore(voteElement);
	parent.append(newCommentHtml);
});

$(document).on("click", "button[class='cancel btn btn-primary']", function(){
	$(this).parent().parent().remove();
});

$(document).on("click", "button[class='submit btn btn-primary']", function(){
	var parentDiv = $(this).parent().parent();
	var textEntered = parentDiv.find(".newcomment-txtarea").val();
	var postId = "";
	var displayName = "Jayaprakash";
	var currentDateTime = moment().format("YYYY-MM-DD HH:mm:ss");
	var containerType = parentDiv.parent().attr('id');
	if(containerType == "questioncomments"){
		postId = getParametersByName("qId");
	}
	else{
		var answerId = parentDiv.parent().find(".answer-comments").attr('id');
		postId = answerId.substring(answerId.lastIndexOf("-")+1);
	}
	if(textEntered.trim()==""){
		//Display a Validation message
		return;
	}
	var postData = {
		"PostId" : postId,
		"Text" : textEntered,
		"DisplayName" : displayName
	};
	$.ajax(
		{
			url: "saveComment",
			contentType: "application/json; charset=utf-8",
			data: JSON.stringify(postData),
			beforeSend: function(xhr){
				
			},
			error: function(xhr){
				
			},
			type: "POST"
		})
		.done(function(data){
			if(data.status == 'successfully saved'){
				var newComment = "<p class = 'comment-p'>";
				newComment = newComment + textEntered;
				newComment = newComment + " - <a href='" + '#' + "'>" + displayName + "</a> " + currentDateTime;
				newComment = newComment + "</p>";
				if(containerType == "questioncomments"){
					var addnew = parentDiv.parent().find(".add-comment-link");
					$(newComment).insertBefore(addnew);
					parentDiv.parent().find(".new-comment-element").remove();
				}
				else{
					var addnew = parentDiv.parent().find(".answer-comments");
					addnew.append(newComment);
					parentDiv.parent().find(".new-comment-element").remove();
				}
				
			}
			else{
				//Some error has occured
			}
		})
		.fail(function(data){
			//Handle the error
		});
});

$(document).on("click", "button[class='post-answer btn btn-primary']", function(){
	var answerHtmlText = CKEDITOR.instances['richtext-area'].getData();
	var questionId = getParametersByName("qId");
	var currentDateTime = moment().format("YYYY-MM-DD HH:mm:ss");
	if(answerHtmlText.trim() == ''){
		var validationMessage = "Your answer couldn't be submitted. Answer is empty.";
		$(this).parent().find(".validation").text(validationMessage);
	}
	else{
		var postData = {
			"QuestionId" : questionId,
			"Body" : answerHtmlText,
			"DisplayName" : "Jayaprakash"		
		};
		$(this).parent().find(".validation").text("");
		$.ajax({
			url: "saveAnswer",
			contentType: "application/json; charset=utf-8",
			data: JSON.stringify(postData),
			beforeSend: function(xhr){
				
			},
			error: function(xhr){
				
			},
			type: "POST"
		})
		.done(function(data){
			if(data.status == "successfully saved"){
				var answerobj = {
					answerid: "",
					answervoteid: "",
					answercontent: "",
					answertime: "",
					ansusername: "",
					answercommentdivid: "",
					answercomments: "",
					userUrl: "",
					usefulnesscount: "",
					upvoteid: "",
					downvoteid: ""
				};

				answerobj.answerid = "answer-" + data.postId;
				answerobj.answervoteid = "answervote-" + data.postId;
				answerobj.answercontent = answerHtmlText;
				answerobj.answertime = currentDateTime;
				answerobj.ansusername = "Jayaprakash";
				answerobj.answercommentdivid = "answer-comments-" + data.postId;
				answerobj.userUrl = "#";
				answerobj.usefulnesscount = 0;
				answerobj.upvoteid = "answerupvote-" + data.postId;
				answerobj.downvoteid = "answerdownvote-" + data.postId;
				
				$("#answercontentcontainer").loadTemplate("/static/templates/answers.html", answerobj, { append: true});
			}
			else{
				//handle error
			}
		})
		.fail(function(){
			//Handle error
		});
	}
});

$(document).on("click", "img[class='emoticon']", function(){
	var parent = $(this).parent();
	
	parent.find("img").each(function(){
		$(this).removeClass("selected-image");
	});
	$(this).addClass("selected-image");
	
	var answerid = parent.prop("id");
	var postId = answerid.substring(answerid.lastIndexOf("-")+1);
	var alt = $(this).prop("alt");
	var ratingScore = -1;
	var userId = 1;
	if(alt == "excited"){
		ratingScore = 10;
	}
	else if(alt == "happy"){
		ratingScore = 7;
	}
	else if(alt == "poker"){
		ratingScore = 2;
	}
	else if(alt == "confused"){
		ratingScore = -3;
	}
	else if(alt == "angry"){
		ratingScore = -5;
	}
	//Now an ajax call to store the rating score given by user
	var url = "saveUserRating";
	var postData = {
			"PostId" : postId,
			"RatingScore" : ratingScore,
			"UserId" : 	userId
		};
	$.ajax(
		{
			url: url,
			contentType: "application/json; charset=utf-8",
			data: JSON.stringify(postData),
			beforeSend: function(xhr){
				
			},
			error: function(xhr){
				
			},
			type: "POST"
		})
		.done(function(data){
			if(data.status == "successfully saved"){
				//Successfully saved
			}
			else{
				console.log("error")
			}
		})
		.fail(function(){
			//Handle error
		});
});