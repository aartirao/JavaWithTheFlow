function login(data) {
	$.ajax({
	  url: "/checkPassword",
	  method: "POST",
	  data: JSON.stringify(data),
	  contentType: 'application/json'
	}).done(function( msg ) {
	  console.log(msg);
	  if(msg.result === 1) {
	  	console.log("success js");
	  	window.location.href = "/mainPage?username="+username;
	  } else{
	  	console.log("done but error");
	  	window.location.href = "/loginPage";
	  }  
	}).fail(function( jqXHR, textStatus ) {
		console.log("error");
	  	window.location.href = "/loginPage";
	});
}

$(document).ready(function () {
	$('.tog').click(function(){
		console.log("works");
	    $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
	});

	$(".login-form").on("click", "#login", function(event){
		event.preventDefault();
		username = $("#username").val();
		password = $("#password").val();

		data = {"username" : username, "password" : password};
		console.log(data);
		login(data);

	});

	$("#create").click(function(){
		event.preventDefault();
		username = $("#newuser").val();
		password = $("#newpwd").val();
		age = $("#age").val();
		about = $("#about").val();

		data = {"username" : username, "password" : password, "age" : age, "about" : about};
		console.log(data);

		$.ajax({
		  url: "/createUser",
		  method: "POST",
		  data: JSON.stringify(data),
		  contentType: 'application/json'
		}).done(function( msg ) {
		  console.log("User logged in");
		  window.location.href = "/mainPage?username="+username;

		}).fail(function( jqXHR, textStatus ) {
		  alert( "Request failed: " + textStatus );
		});
	});
});