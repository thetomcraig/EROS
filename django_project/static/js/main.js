console.log("alpha");

$(function () {
  $("#drugs").autocomplete({
    source: "get_drugs/" 
  });
});
