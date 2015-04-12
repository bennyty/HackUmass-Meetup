$(document).ready(function() {
    var openPanel = $('#one');
    $(document).on("click", openPanel.attr('.class1'), function() {
        var newPanel = openPanel.clone();
	$('div').after(newPanel);
        if (openPanel.val("id") == "two") {
            newPanel.attr("id", "three");
        } else {
            newPanel.attr("id", "two");
        }
	newPanel.animate({left: "+=100px"}, 250);
        openPanel = newPanel;
    });
});