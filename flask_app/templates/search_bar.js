var blends = {{search_list}}
var results_element = document.getElementById('search_results');
function search_blends() {

    var query = document.getElementById("search_bar").value.toLowerCase();
    console.log(query);
    console.log(results_element.classList);
    if (query == "" && results_element.classList.contains("show")){
        $("#search_results").dropdown('hide');
        return;
    }
    var new_inner_html = "";
    var results = 0;

    for (var i = 0; i < blends.length; i++) {
        var index = blends[i].text.indexOf(query);
        if (index > -1) {
            var txt = blends[i].full_text
            txt = txt.slice(0, index) + "<b>" + txt.slice(index, index+query.length) + "</b>" +txt.slice(index+query.length);
            new_inner_html += "<a class='dropdown-item' href='/individual_blends/" + blends[i].key + "'>" + txt + "</a>";
            results += 1
            if (results >= 10) { break; }
        }
    }
    if (new_inner_html != "" && !results_element.classList.contains("show")){
        console.log("show")
        $("#search_results").dropdown('show');
    }
    results_element.innerHTML = new_inner_html;
}