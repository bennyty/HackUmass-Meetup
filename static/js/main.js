$(document).ready(function() {

    var panelOne = $('#panelOne');
    var panelTwo = $('#panelTwo');
    var panelThree = $('#panelThree');

    var classList = [];
    $.getJSON('/rpi.json', function(data) {
	for (var i in data.classes) {
	    classList[i] = data.classes[i].department + " " + data.classes[i].number + ": " + data.classes[i].name;
	}
    });
    
    $("#autocomplete").autocomplete({
	minLength: 2,
	source: classList
    });
    
    $("#autocomplete").keypress(function(e) {
    if(e.keyCode == 13)
	{
	    var input = $('#autocomplete').val().split(" ", 3);
	    
	    
	    
	//    $.getJSON('https://raw.githubusercontent.com/bennyty/HackUmass-Meetup/master/rpi.json', function(data) {
	//	for (var i in data.classes) {
	//	    if (data.classes[i].department == input[0] && data.classes[i].number == input[1]) {
	//		//code
	//	    }
	//	}
	//    });
	    
	    
	    $('body div ul').append("<li>" + $('#autocomplete').val() + "</li>");
	    
	    
	    
	}
    });
    
    //LINK HOVERS
    $(document).on("mouseenter", ".open ul li a", function() {
	$(this).css("background", "#999999");
	$(this).children("div").css("color", "#fff");
    });
    $(document).on("mouseleave", ".open ul li a", function() {
	$(this).css("background", "#f3f3f3");
	$(this).children("div").css("color", "#666");
    });
    
    
    //CLOSED PANEL HOVERS
    $(document).on("mouseenter", ".closed", function() {
	$(this).fadeTo(100, 0.8);
    });
    $(document).on("mouseleave", ".closed", function() {
	$(this).fadeTo(100, 0.5);
    })
    
    
    //PANEL OPENINGS
    $(document).on("click", "#panelOne.open ul li a", function() {
        //PANEL MOVEMENT
	panelTwo.css("left", "0px");
	panelTwo.fadeIn({queue: false, duration: 250});
	panelTwo.animate({left: "+=200px", opacity: "1"}, 250);
        panelOne.fadeTo(300, 0.5);
        
        panelOne.attr("class", "panel closed");
        panelTwo.attr("class", "panel open");
	
	//PANEL DATA POPULATION
	var title = $(this).children("div:first").html();
	$('#panelTwo h3').replaceWith("<h3>" + title + "</h3>");
	
	//$.getJSON("document.json", function(data) {
	//    var output;
	//    for (var i in data.classes) {
	//	output += "classes."
	//	
	//	output+="<li>" + data.users[i].firstName + " " + data.users[i].lastName + "--" + data.users[i].joined.month+"</li>";
	//    }
	//});
    });
    
    $(document).on("click", "#panelTwo.open ul li a", function() {
	panelThree.css("left", "200px");
	panelThree.fadeIn({queue: false, duration: 250});
        panelThree.animate({left: "+=200px", opacity: "1"}, 250);
        panelTwo.fadeTo(300, 0.5);
        panelOne.fadeTo(300, 0.5);
        
        panelTwo.attr("class", "panel closed");
        panelThree.attr("class", "panel open");
    });
    
    
    //PANEL CLOSINGS
    $(document).on("click", "#panelTwo.closed", function() {
	panelThree.fadeOut({queue: false, duration: 250});
	panelThree.animate({left: "+=200px"}, 250)
	panelThree.attr("class", "panel closed");
	panelTwo.attr("class", "panel open");
	panelTwo.fadeTo(250, 1);
	
	$('.open ul li a').css("background", "#f3f3f3");
	$('.open ul li a').children("div").css("color", "#666");
    });
    
    $(document).on("click", "#panelOne.closed", function() {
	if (panelThree.is(".open")) {
	    panelThree.fadeOut({queue: false, duration: 250});
	    panelThree.animate({left: "+=200px"}, 250);
	    panelThree.attr("class", "panel closed");
	    
	    panelTwo.fadeOut({queue: false, duration: 250});
	    panelTwo.animate({left: "+=200px"}, 250);
	    panelTwo.attr("class", "panel closed");
	} else {
	    panelTwo.fadeOut({queue: false, duration: 250});
	    panelTwo.animate({left: "+=200px"}, 250);
	    panelTwo.attr("class", "panel closed");
	}
	
	panelOne.fadeTo(250, 1);
	panelOne.attr("class", "panel open");
	
	$('.panel ul li a').css("background", "#f3f3f3");
	$('.panel ul li a').children("div").css("color", "#666");
    });
});