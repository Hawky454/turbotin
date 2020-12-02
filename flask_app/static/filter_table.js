function toggle_stock() {
    var check_box = document.getElementById("in_stock_check");
    if (check_box.classList.contains("active")) {
        check_box.classList.remove("active");
    } else {
        check_box.classList.add("active");
    }
    filter_table();
}

function toggle_sort() {
    var button = document.getElementById("price_sort");
    if (button.dataset.sort_direction == "asc") {
        button.dataset.sort_direction = "desc";
        button.innerHTML = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-arrow-down" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M8 1a.5.5 0 0 1 .5.5v11.793l3.146-3.147a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 .708-.708L7.5 13.293V1.5A.5.5 0 0 1 8 1z"/></svg>';
    } else {
        button.dataset.sort_direction = "asc";
        button.innerHTML = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-arrow-up" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M8 15a.5.5 0 0 0 .5-.5V2.707l3.146 3.147a.5.5 0 0 0 .708-.708l-4-4a.5.5 0 0 0-.708 0l-4 4a.5.5 0 1 0 .708.708L7.5 2.707V14.5a.5.5 0 0 0 .5.5z"/></svg>';
    }
    sort_table(6);
}

function search_filter(filter, td) {
    return (td.textContent || td.innerText).toUpperCase().indexOf(filter) > -1
}

function stock_filter(active, td) {
    return !(active && (td.textContent || td.innerText) == "Out of stock")
}

function filter_table() {
    var table = document.getElementById("myTable");
    var tr = table.getElementsByTagName("tr");
    var stock_check_active = document.getElementById("in_stock_check").classList.contains("active");
    var filter_item = input = document.getElementById("search_form_item").value.toUpperCase();
    var filter_store = input = document.getElementById("search_form_store").value.toUpperCase();
    var num_results = 0;

    for (var i = 0; i < tr.length; i++) {

        td_stock = tr[i].getElementsByTagName("td")[2];
        td_item = tr[i].getElementsByTagName("td")[1];
        td_store = tr[i].getElementsByTagName("td")[0];

        if (td_item && td_stock) {
            if (search_filter(filter_item, td_item) && stock_filter(stock_check_active, td_stock) && search_filter(filter_store, td_store)) {
                tr[i].dataset.filtered = false;
                num_results += 1;
                if (num_results > 101){
                    tr[i].style.display = "none";
                } else {
                    tr[i].style.display = "";
                }
            } else {
                tr[i].dataset.filtered = true;
                tr[i].style.display = "none";
            }
        }
    }
    console.log($('#myTable tr:visible').length);
    hidden_alert();
}