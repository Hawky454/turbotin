var blends = {{search_list}}
function search_blends() {
    var query = document.getElementById("search_bar").value.toLowerCase();
    var results_element = document.getElementById('search_results');
    if (query == ""){
        results_element.classList.remove("show");
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

    if (results > 0){
        results_element.classList.add("show");
    } else{
        results_element.classList.remove("show");
    }
    results_element.innerHTML = new_inner_html;
}