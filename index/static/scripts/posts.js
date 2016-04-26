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

function getLevel(counts, value) {
	counts = counts.sort(function (a, b) { return a - b });

	var returnValue = 0;
	var i = 0;
	for (index = 0; index < counts.length; ++index) {
		i = i + 1;
		if (counts[index] == value) {
			returnValue = i;
			break;
		}
	}
	return returnValue;
}

function setClassForImage(initialclass, counts, value, userValue) {
	var level = getLevel(counts, value);
	if (level == 5) {
		initialclass = initialclass + " opacity-one";
	}
	else if (level == 4) {
		initialclass = initialclass + " opacity-two";
	}
	else if (level == 3) {
		initialclass = initialclass + " opacity-three";
	}
	else if (level == 2) {
		initialclass = initialclass + " opacity-four";
	}
	else if (level == 1) {
		initialclass = initialclass + " opacity-five";
	}

	return initialclass;
}

$(document).ready(function () {
	var questionId = getParametersByName("qId");
	var url = "getQuestion";
	var userId = 1
	url = url + "/" + questionId + "/" + userId;

	var url1 = "updateViewCount";

	data = { "PostId": questionId };
	$.ajax(
		{
			url: url1,
			beforeSend: function (xhr) {

			},
			error: function (xhr) {

			},
			method: "POST",
			data: JSON.stringify(data),
			contentType: 'application/json',
		})
		.fail(function () {
			//Handle the error

		});
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

			var titleContent = json.question.postTitle;
			if (json.question.isBookMarked == 1) {
				titleContent = "<i id = 'bookmarked' class='fa fa-bookmark fa-lg' aria-hidden='true'></i>" + titleContent;
			}
			else {
				titleContent = "<i id = 'bookmarked' class='fa fa-bookmark-o fa-lg' aria-hidden='true'></i>" + titleContent;
			}
			$("#qTitle").html(titleContent);
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
					downvoteid: "",
					isExcited: "",
					isHappy: "",
					isPoker: "",
					isConfused: "",
					isAngry: "",
					excitedCount: "",
					pokerCount: "",
					angryCount: "",
					happyCount: "",
					confusedCount: ""
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

				//Change later
				var countArray = [];
				countArray.push(answeritem.answer.excitedCount);
				countArray.push(answeritem.answer.happyCount);
				countArray.push(answeritem.answer.neutralCount);
				countArray.push(answeritem.answer.confusedCount);
				countArray.push(answeritem.answer.angryCount);
				//To set the class
				var isAngry = "emoticon" + " width-five";
				var isConfused = "emoticon" + " width-five";
				var isExcited = "emoticon" + " width-five";
				var isHappy = "emoticon" + " width-five";
				var isPoker = "emoticon" + " width-five";
				//console.log(countArray);
				isAngry = setClassForImage(isAngry, countArray, answeritem.answer.angryCount);
				isConfused = setClassForImage(isConfused, countArray, answeritem.answer.confusedCount);
				isExcited = setClassForImage(isHappy, countArray, answeritem.answer.excitedCount);
				isHappy = setClassForImage(isHappy, countArray, answeritem.answer.happyCount);
				isPoker = setClassForImage(isPoker, countArray, answeritem.answer.neutralCount);

				//Change later

				if (answeritem.answer.currentUserRating == 10) {
					isExcited = isExcited + " selected-image";
				}
				else if (answeritem.answer.currentUserRating == 7) {
					isHappy = isHappy + " selected-image";
				}
				else if (answeritem.answer.currentUserRating == 2) {
					isPoker = isPoker + " selected-image";
				}
				else if (answeritem.answer.currentUserRating == -3) {
					isConfused = isConfused + " selected-image";
				}
				else if (answeritem.answer.currentUserRating == -5) {
					isAngry = isAngry + " selected-image";
				}

				answerobj.isAngry = isAngry;
				answerobj.isConfused = isConfused;
				answerobj.isExcited = isExcited;
				answerobj.isHappy = isHappy;
				answerobj.isPoker = isPoker;

				answerobj.angryCount = answeritem.answer.angryCount;
				answerobj.happyCount = answeritem.answer.happyCount;
				answerobj.excitedCount = answeritem.answer.excitedCount;
				answerobj.confusedCount = answeritem.answer.confusedCount;
				answerobj.pokerCount = answeritem.answer.neutralCount;
				//20, 17, 15, 10, 7

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

			$.each(answerArray, function (key, ans) {
				var ansid = ans.answervoteid;
				$("#" + ansid).find("img[alt='excited']").attr("title", ans.excitedCount);
				$("#" + ansid).find("img[alt='happy']").attr("title", ans.happyCount);
				$("#" + ansid).find("img[alt='poker']").attr("title", ans.pokerCount);
				$("#" + ansid).find("img[alt='confused']").attr("title", ans.confusedCount);
				$("#" + ansid).find("img[alt='angry']").attr("title", ans.angryCount);



				/*$("#"+ansid).find("img[alt='excited']").tooltip({ content: ans.excitedCount});
				$("#"+ansid).find("img[alt='happy']").tooltip({ content: ans.happyCount});
				$("#"+ansid).find("img[alt='poker']").tooltip({ content: ans.pokerCount});
				$("#"+ansid).find("img[alt='confused']").tooltip({ content: ans.confusedCount});
				$("#"+ansid).find("img[alt='angry']").tooltip({ content: ans.angryCount});*/

			});
		})
		.fail(function () {
			//Handle the error

		});

	//Adding richtext editor
	CKEDITOR.replace('richtext-area');
	//Update the data on the browser events table
	var browserEventData = {
		"UserId": 1,
		"PostId": questionId,
		"UserName": "Jayaprakash"
	}
	$.ajax(
		{
			url: "updateTime",
			contentType: "application/json; charset=utf-8",
			data: JSON.stringify(browserEventData),
			beforeSend: function (xhr) {

			},
			error: function (xhr) {

			},
			type: "POST"
		})
		.done(function (data) {
			if (data.status == "successfully saved") {
			}
			else {
			}
		})
		.fail(function () {

		});
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

$(document).on("click", "button[class='cancel btn btn-primary']", function () {
	$(this).parent().parent().remove();
});

$(document).on("click", "button[class='submit btn btn-primary']", function () {
	var parentDiv = $(this).parent().parent();
	var textEntered = parentDiv.find(".newcomment-txtarea").val();
	var postId = "";
	var displayName = "Jayaprakash";
	var currentDateTime = moment().format("YYYY-MM-DD HH:mm:ss");
	var containerType = parentDiv.parent().attr('id');
	if (containerType == "questioncomments") {
		postId = getParametersByName("qId");
	}
	else {
		var answerId = parentDiv.parent().find(".answer-comments").attr('id');
		postId = answerId.substring(answerId.lastIndexOf("-") + 1);
	}
	if (textEntered.trim() == "") {
		//Display a Validation message
		return;
	}
	var postData = {
		"PostId": postId,
		"Text": textEntered,
		"DisplayName": displayName
	};
	$.ajax(
		{
			url: "saveComment",
			contentType: "application/json; charset=utf-8",
			data: JSON.stringify(postData),
			beforeSend: function (xhr) {

			},
			error: function (xhr) {

			},
			type: "POST"
		})
		.done(function (data) {
			if (data.status == 'successfully saved') {
				var newComment = "<p class = 'comment-p'>";
				newComment = newComment + textEntered;
				newComment = newComment + " - <a href='" + '#' + "'>" + displayName + "</a> " + currentDateTime;
				newComment = newComment + "</p>";
				if (containerType == "questioncomments") {
					var addnew = parentDiv.parent().find(".add-comment-link");
					$(newComment).insertBefore(addnew);
					parentDiv.parent().find(".new-comment-element").remove();
				}
				else {
					var addnew = parentDiv.parent().find(".answer-comments");
					addnew.append(newComment);
					parentDiv.parent().find(".new-comment-element").remove();
				}

			}
			else {
				//Some error has occured
			}
		})
		.fail(function (data) {
			//Handle the error
		});
});

$(document).on("click", "button[class='post-answer btn btn-primary']", function () {
	var answerHtmlText = CKEDITOR.instances['richtext-area'].getData();
	var questionId = getParametersByName("qId");
	var currentDateTime = moment().format("YYYY-MM-DD HH:mm:ss");
	if (answerHtmlText.trim() == '') {
		var validationMessage = "Your answer couldn't be submitted. Answer is empty.";
		$(this).parent().find(".validation").text(validationMessage);
	}
	else {
		var postData = {
			"QuestionId": questionId,
			"Body": answerHtmlText,
			"DisplayName": "Jayaprakash"
		};
		$(this).parent().find(".validation").text("");
		$.ajax({
			url: "saveAnswer",
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

					$("#answercontentcontainer").loadTemplate("/static/templates/answers.html", answerobj, { append: true });
				}
				else {
					//handle error
				}
			})
			.fail(function () {
				//Handle error
			});
	}
});

$(document).on("click", "img[class='emoticon']", function () {
	var parent = $(this).parent();

	parent.find("img").each(function () {
		$(this).removeClass("selected-image");
	});
	$(this).addClass("selected-image");

	var answerid = parent.prop("id");
	var postId = answerid.substring(answerid.lastIndexOf("-") + 1);
	var alt = $(this).prop("alt");
	var ratingScore = -1;
	var userId = 1;
	if (alt == "excited") {
		ratingScore = 10;
	}
	else if (alt == "happy") {
		ratingScore = 7;
	}
	else if (alt == "poker") {
		ratingScore = 2;
	}
	else if (alt == "confused") {
		ratingScore = -3;
	}
	else if (alt == "angry") {
		ratingScore = -5;
	}
	//Now an ajax call to store the rating score given by user
	var url = "saveUserRating";
	var postData = {
		"PostId": postId,
		"RatingScore": ratingScore,
		"UserId": userId
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
				//Successfully saved
			}
			else {

			}
		})
		.fail(function () {
			//Handle error
		});
});

$(document).on("click", "i[id = 'bookmarked']", function () {
	var url = "/bookmark";
	var questionId = getParametersByName("qId");
	var postData = {
		"UserId": 1,
		"PostId": questionId
	};
	var classname = $(this).attr("class");
	var element = $(this);
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
				if (classname == "fa fa-bookmark-o fa-lg") {
					element.removeClass("fa fa-bookmark-o fa-lg");
					element.addClass("fa fa-bookmark fa-lg");
				}
				else {
					element.removeClass("fa fa-bookmark fa-lg");
					element.addClass("fa fa-bookmark-o fa-lg");
				}
			}
			else {
				//handle error
			}
		})
		.fail(function () {
			//Handle error
		});
});

//Event to update the text selection action
function getSelectionText() {
	var text = "";
	if (window.getSelection) {
		text = window.getSelection().toString();
	} else if (document.selection && document.selection.type != "Control") {
		text = document.selection.createRange().text;
	}
	return text;
}

$(document).on("click", "td[class = 'answercell']", function(){
	var selectedText = getSelectionText();
	console.log("select");
	console.log(selectedText);
	if(selectedText.trim() == ""){
		return;
	}
	
	var postId = $(this).find(".voters").attr("id");
	postId = postId.substring(postId.lastIndexOf("-") + 1);
	console.log(postId);
	var postData = {
		"PostId" : postId,
		"PostTypeId": 2,
		"UserId": 1,
		"UserName": "Jayaprakash"
	};
	$.ajax(
		{
			url: "updateSelectAction",
			contentType: "application/json; charset=utf-8",
			data: JSON.stringify(postData),
			beforeSend: function (xhr) {

			},
			error: function (xhr) {

			},
			type: "POST"
		})
		.done(function(data){
			if(data.status == "successfully saved"){
				console.log("Success");
			}
			else{
				console.log("Error");
			}
			
		})
		.fail(function(){
			
		});
});

$(document).on("click", "div[id = 'questioncontainer']", function(){
	var selectedText = getSelectionText();
	console.log("select");
	console.log(selectedText);
	if(selectedText.trim() == ""){
		return;
	}
	
	var postId = getParametersByName("qId");
	console.log(postId);
	var postData = {
		"PostId" : postId,
		"PostTypeId": 1,
		"UserId": 1,
		"UserName": "Jayaprakash"
	};
	$.ajax(
		{
			url: "updateSelectAction",
			contentType: "application/json; charset=utf-8",
			data: JSON.stringify(postData),
			beforeSend: function (xhr) {

			},
			error: function (xhr) {

			},
			type: "POST"
		})
		.done(function(data){
			if(data.status == "successfully saved"){
				console.log("Success");
			}
			else{
				console.log("Error");
			}
			
		})
		.fail(function(){
			
		});
});