function update_search(id, items, dropdown_element) {
    var results_element = document.getElementById(id + '_results');
    var input_element = document.getElementById(id + "_input");
    var query = input_element.value.toLowerCase();
    results_element.innerHTML = "";
    var results = 0;
    var max_results = 50;
    for (var i = 0; i < items.length; i++) {
        if (results > max_results) {
            results_element.innerHTML += `<li class='dropdown-item text-secondary'> Only showing first ${max_results} results</li>`
            break;
        }
        var index = items[i].text.toLowerCase().indexOf(query);
        if (index > -1) {
            var txt = items[i].text
            txt = txt.slice(0, index) + "<b>" + txt.slice(index, index + query.length) + "</b>" + txt.slice(index + query.length);
            results_element.innerHTML += `<li><a class="dropdown-item" href="${items[i].link}">${txt}</a></li>`;
            results++;
        }

    }
    if (results_element.innerHTML === "") {
        results_element.innerHTML = "<small class='dropdown-item disabled'>No results found</small>"
        if (input_element.classList.contains("show"))
            dropdown_element.hide();
    } else {
        if (!input_element.classList.contains("show") && input_element === document.activeElement)
            dropdown_element.show();
    }
    return true;
}
