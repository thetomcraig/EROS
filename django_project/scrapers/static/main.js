$(".btn").click(function() {
    console.log("alpha");
    if($("#collapseme").hasClass("out")) {
        $("#collapseme").addClass("in");
        $("#collapseme").removeClass("out");
    } else {
        $("#collapseme").addClass("out");
        $("#collapseme").removeClass("in");
    }
});
