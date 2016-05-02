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
var userIdglobal = ""

function getParametersByName(name, url) {
	if (!url) url = window.location.href;
	name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)", "i"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}
var userName = "";

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
	var username = getParametersByName("username");
	var url = "getQuestion";
	$.ajax({
		url: '/getUserId/' + username, success: function (result) {
			userIdglobal = result.result;
			//console.log("Scuccess" + userIdglobal);
			$("#hiddenField").val(result.result);

			userIdglobal = $("#hiddenField").val();

			userName = getParametersByName("username");

			url = url + "/" + questionId + "/" + userIdglobal;
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

					//console.log(json);
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

					var acceptedAnswerId = -1;
					if (json.question.acceptedAnswerId != null) {
						acceptedAnswerId = json.question.acceptedAnswerId;
					}
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
					//Set Accepted answer
					//console.log(acceptedAnswerId);
					if (acceptedAnswerId != -1) {
						var elem = $("#answer-" + acceptedAnswerId).find(".answer-text");
						var acceptedhtml = "<div><i class='fa fa-check fa-lg' aria-hidden='true'></i></div>"
						$(acceptedhtml).insertBefore(elem);
					}

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
				"UserId": userIdglobal,
				"PostId": questionId,
				"UserName": userName//"Jayaprakash"
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

			jQuery.ajaxSetup({
				beforeSend: function () {
					$('#loader').show();
				},
				complete: function () {
					$('#loader').hide();
				},
				success: function () { }
			});
		}
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
	var displayName = userName//"Jayaprakash";
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
				
				newComment = newComment + " - <a href='" + "/profile?uId=" + userIdglobal + "&cId="+userIdglobal +"'>" + displayName + "</a> " + currentDateTime;
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
			"DisplayName": userName//"Jayaprakash"
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

					answerobj.answerid = "answer-" + data.postId;
					answerobj.answervoteid = "answervote-" + data.postId;
					answerobj.answercontent = answerHtmlText;
					answerobj.answertime = currentDateTime;
					answerobj.ansusername = userName//"Jayaprakash";
					answerobj.answercommentdivid = "answer-comments-" + data.postId;
					answerobj.userUrl = "/profile?uId="+userIdglobal+"&cId="+userIdglobal;
					answerobj.usefulnesscount = 0;
					answerobj.upvoteid = "answerupvote-" + data.postId;
					answerobj.downvoteid = "answerdownvote-" + data.postId;

					var isAngry = "emoticon" + " width-five opacity-five";
					var isConfused = "emoticon" + " width-five opacity-five";
					var isExcited = "emoticon" + " width-five opacity-five";
					var isHappy = "emoticon" + " width-five opacity-five";
					var isPoker = "emoticon" + " width-five opacity-five";

					answerobj.isAngry = isAngry;
					answerobj.isConfused = isConfused;
					answerobj.isExcited = isExcited;
					answerobj.isHappy = isHappy;
					answerobj.isPoker = isPoker;

					answerobj.angryCount = 0;
					answerobj.happyCount = 0;
					answerobj.excitedCount = 0;
					answerobj.confusedCount = 0;
					answerobj.pokerCount = 0;

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

$(document).on("click", "img", function () {
	//console.log("success");
	var parent = $(this).parent();
	//console.log(userIdglobal);
	if ($(this).hasClass("selected-image")) {
		//do nothing
	}
	else {
		var existingrate = parseInt($(this).attr("title"));
		$(this).attr("title", existingrate + 1);
	}
	parent.find("img").each(function () {
		$(this).removeClass("selected-image");
	});
	$(this).addClass("selected-image");

	var answerid = parent.prop("id");
	var postId = answerid.substring(answerid.lastIndexOf("-") + 1);
	var alt = $(this).prop("alt");
	var ratingScore = -1;
	var userId = userIdglobal;
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
		"UserId": userIdglobal,
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

$(document).on("click", "td[class = 'answercell']", function () {
	var selectedText = getSelectionText();
	//console.log("select");
	//console.log(selectedText);
	if (selectedText.trim() == "") {
		return;
	}

	var postId = $(this).find(".voters").attr("id");
	postId = postId.substring(postId.lastIndexOf("-") + 1);
	//console.log(postId);
	var postData = {
		"PostId": postId,
		"PostTypeId": 2,
		"UserId": userIdglobal,
		"UserName": userName//"Jayaprakash"
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
		.done(function (data) {
			if (data.status == "successfully saved") {
				//console.log("Success");
			}
			else {
				//console.log("Error");
			}

		})
		.fail(function () {

		});
});

$(document).on("click", "div[id = 'questioncontainer']", function () {
	var selectedText = getSelectionText();
	//console.log("select");
	//console.log(selectedText);
	if (selectedText.trim() == "") {
		return;
	}

	var postId = getParametersByName("qId");
	//console.log(postId);
	var postData = {
		"PostId": postId,
		"PostTypeId": 1,
		"UserId": userIdglobal,
		"UserName": userName//"Jayaprakash"
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
		.done(function (data) {
			if (data.status == "successfully saved") {
				//console.log("Success");
			}
			else {
				//console.log("Error");
			}

		})
		.fail(function () {

		});
});