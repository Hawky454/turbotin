var blends = {{search_list}}
var results_element = document.getElementById('search_results');
var count = 0;
function search_blends() {
    var query = document.getElementById("search_bar").value.toLowerCase();
    count += 1;

    if (query == ""){
        results_element.innerHTML = "";
        results_element.classList.add("p-0", "m-0", "border-0")
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
    if (new_inner_html != "") {
        results_element.classList.remove("p-0", "m-0", "border-0")
        if ($("#search_bar").is(':hover') && !results_element.classList.contains("show")) {
            $("#search_bar").trigger("click");
        }
    } else {
        results_element.classList.add("p-0", "m-0", "border-0")
    }
    results_element.innerHTML = new_inner_html;
    return true;
}