$(document).ready(function() {

    var panelOne = $('#panelOne');
    var panelTwo;

    //var openPanel = panelOne;

    $(document).on("mouseenter", ".open ul li a", function() {
	$(this).css("background", "#999999");
	$(this).css("color", "#fff");
    });
    $(document).on("mouseleave", ".open ul li a", function() {
	$(this).css("background", "#eeeeee");
	$(this).css("color", "#999");
    })
    
    $(document).on("click", "#panelOne.open ul li a", function() {
	    panelTwo = panelOne.clone();
	    panelTwo.attr("id", "panelTwo");
	    panelOne.after(panelTwo);
	    
	    panelTwo.animate({left: "+=100px"}, 250);
	    panelOne.fadeTo(300, 0.6);
	    
	    panelOne.attr("class", "panel closed");
	    panelTwo.attr("class", "panel open");
    });
    
    $(document).on("click", "#panelTwo.open ul li a", function() {
	    var panelThree = panelTwo.clone();
	    panelThree.attr("id", "panelThree");
	    panelTwo.after(panelThree);
	    
	    panelThree.animate({left: "+=100px"}, 250);
	    panelTwo.fadeTo(300, 0.6);
	    panelOne.fadeTo(300, 0.3);
	    
	    panelTwo.attr("class", "panel closed");
	    panelThree.attr("class", "panel open");
    });
    
});