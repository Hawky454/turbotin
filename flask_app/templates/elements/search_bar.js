function update_search(id, items, dropdown_element) {
    var results_element = document.getElementById(id + '_results');
    var input_element = document.getElementById(id + "_input");
    var query = input_element.value.toLowerCase();
    var new_inner_html = "";

    for (var i = 0; i < items.length; i++) {
        var index = items[i].toLowerCase().indexOf(query);
        if (index > -1) {
            var txt = items[i]
            txt = txt.slice(0, index) + "<b>" + txt.slice(index, index + query.length) + "</b>" + txt.slice(index + query.length);
            new_inner_html += `<li><a class="dropdown-item" href="#">${txt}</a></li>`;
        }
    }
    results_element.innerHTML = new_inner_html;
    if (new_inner_html === "") {
        if (input_element.classList.contains("show"))
            dropdown_element.hide();
    } else {
        if (!input_element.classList.contains("show") && input_element === document.activeElement)
            dropdown_element.show();
    }
    return true;
}
