$(document).ready(function() {

    var panelOne = $('#panelOne');
    var panelTwo = $('#panelTwo');
    var panelThree = $('#panelThree');

    $( ".selector" ).autocomplete({
    position: { my : "center"}
    });
    
    //LINK HOVERS
    $(document).on("mouseenter", ".open ul li a", function() {
	$(this).css("background", "#999999");
	$(this).css("color", "#fff");
    });
    $(document).on("mouseleave", ".open ul li a", function() {
	$(this).css("background", "#eeeeee");
	$(this).css("color", "#999");
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
	panelTwo.fadeIn({queue: false, duration: 250});
	panelTwo.animate({left: "+=200px"}, 250);
        panelOne.fadeTo(300, 0.5);
        
        panelOne.attr("class", "panel closed");
        panelTwo.attr("class", "panel open");
	
	//PANEL DATA POPULATION
	$.getJSON("catalog.json", function(data) {
	    
	});
    });
    
    $(document).on("click", "#panelTwo.open ul li a", function() {
	panelThree.fadeIn({queue: false, duration: 250});
        panelThree.animate({left: "+=200px"}, 250);
        panelTwo.fadeTo(300, 0.5);
        panelOne.fadeTo(300, 0.5);
        
        panelTwo.attr("class", "panel closed");
        panelThree.attr("class", "panel open");
    });
    
    
    //PANEL CLOSINGS
    $(document).on("click", "#panelTwo.closed", function() {
	panelThree.animate({left: "+=200px", opacity: "0"}, 250)
	panelThree.attr("class", "panel closed");
	panelTwo.attr("class", "panel open");
	panelTwo.fadeTo(250, 1);
    });
    
    $(document).on("click", "#panelOne.closed", function() {
	if (panelThree.is(".open")) {
	    panelThree.fadeOut({queue: false, duration: 250});
	    panelThree.animate({left: "+=200px"}, 250);
	    panelThree.attr("class", "panel closed");
	    
	    panelTwo.fadeOut({queue: false, duration: 250});
	    panelTwo.animate({left: "+=200px"}, 250);
	    panelTwo.attr("class", "panel closed");
	    
	    panelOne.fadeTo(250, 1);
	    panelOne.attr("class", "panel open");
	} else {
	    panelTwo.fadeOut({queue: false, duration: 250});
	    panelTwo.animate({left: "+=200px"}, 250);
	    panelTwo.attr("class", "panel closed");
	    
	    panelOne.fadeTo(250, 1);
	    panelOne.attr("class", "panel open");
	}
    });
});