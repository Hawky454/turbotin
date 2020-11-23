var documents = {{blends_list}}
var idx = lunr(function () {
  this.ref('key')
  this.field('text')

  documents.forEach(function (doc) {
    this.add(doc)
  }, this)
})
$( "#search_bar" ).keyup(function() {
  var query = $(this).val().toLowerCase();
  if (query.length > 2){
      var result_list = idx.search(query);
      var new_inner_html = "";
      for (var i = 0; i < result_list.length; i++) {
        var result = documents[parseInt(result_list[i].ref)];
        new_inner_html += "<a class='dropdown-item' href='/blends/" + result.key + "'>" + result.full_text + "</a>";
      }
      var results_element = document.getElementById('search_results');
      if (result_list.length > 0){
        results_element.classList.add("show");
      } else{
        results_element.classList.remove("show");
      }
      results_element.innerHTML = new_inner_html;
  }
});