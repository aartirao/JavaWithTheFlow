defaults = {
    callback      : function() {}
  , decimal       : false
  , disable       : false
  , disableOpacity: 0.5
  , hideRange     : false
  , klass         : ''
  , min           : 0
  , max           : 10
  , start         : 5
  , step          : null
  , vertical      : false
};


var answerArray = [];


$(document).ready(function(){
	$.getJSON("static/data/question.json", function(json){
		$("#qTitle").html(json.question.postTitle);
		$("#userdetail").html("by <a href='"+json.question.askedUserProfile+"'>" + json.question.askedbyUserName + "</a>");
		$("#askedtime").html("<span class='glyphicon glyphicon-time'></span> " + json.question.askedDate);
		$("#qtext").html(json.question.postText);
		var commentHtml = "";
		$.each(json.comments, function(key, comment){
			var cHtml = "<p class='comment-p'>";
			cHtml = cHtml + comment.commentText;
			cHtml = cHtml + " - <a href='"+ comment.userUrl + "'>" + comment.commentedUser + "</a>";
			cHtml = cHtml + " " + comment.commentedTime + "</p>";
			commentHtml = commentHtml + cHtml;
		});
		commentHtml = commentHtml + "<a class='add-comment-link' href='#'>add a comment</a>"
		$("#questioncomments").html(commentHtml);


		$("#answercontainer .answerheader h3").text(json.question.noOfAnswers + " Answers");
		$.each(json.answers, function(key, answeritem){
			var answerobj = {
				answerid : "",
				answervoteid : "",
				answercontent : "",
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

			$.each(answeritem.comments, function(ckey, comment){
				var cHtml = "<p class='comment-p'>";
				cHtml = cHtml + comment.commentText;
				cHtml = cHtml + " - <a href='"+ comment.userUrl + "'>" + comment.commentedUser + "</a>";
				cHtml = cHtml + " " + comment.commentedTime + "</p>";
				answercommentHtml = answercommentHtml + cHtml;
			});

			answerobj.answercomments = answercommentHtml;
			answerArray.push(answerobj);

		});
	$("#answercontentcontainer").loadTemplate("static/templates/answers.html", answerArray);

	});

	$(document).on('click', '.vote-up', function(e){
		var element = $(this).parent();
		var id = element.prop("id");
		var flag = 0;
		id = id.substring(id.indexOf('-')+1);
		id = "#answerupvote-"+id;
		if(element.find(".slider-wrapper").hasClass( "hide" )){
			element.find(".slider-wrapper").removeClass( "hide" );
			flag = 1;
		}	
		var upvoteslider = document.querySelector(id);

		if(flag == 1){
			var initupvote = new Powerange(upvoteslider, defaults);
		}	

		upvoteslider.onchange = function(){
			//console.log(upvoteslider.value);
		};
	});

	$(document).on('click', '.vote-down', function(e){
		var element = $(this).parent();
		var id = element.prop("id");
		var flag = 0;
		id = id.substring(id.indexOf('-')+1);
		id = "#answerdownvote-"+id;
		if(element.find(".slider-wrapper-downvote").hasClass( "hide" )){
			element.find(".slider-wrapper-downvote").removeClass( "hide" );
			flag = 1;
		}	
		var downvoteslider = document.querySelector(id);
		if(flag == 1){
			var initdownvote = new Powerange(downvoteslider, defaults);
		}
		downvoteslider.onchange = function(){
			//console.log(downvoteslider.value);
		};			
	});



});
