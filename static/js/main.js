console.log("loaded the js");

$('#target').click(divFunction);

function divFunction(){
 //some code
}

$(function() {
  $("#drugs").autocomplete({
    source: "get_drugs",
    minLength: 2,
  });
});
