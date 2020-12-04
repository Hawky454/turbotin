var max_num_rows = 50;
var table_array = {{table}};

function show_more() {
    max_num_rows += 100;
    filter_table();
    hidden_alert();
}

function hidden_alert() {
    var alert_container = $("#alert_container");
    if ($('#myTable tr:visible').length > max_num_rows) {
        $("#alert").text("Only showing first " + max_num_rows + " rows");
        alert_container.show();
    } else {
        alert_container.hide();
    }
}


function sort_table() {
    hidden_alert();
    var num_results = 0;
    var tr = document.getElementById("myTable").getElementsByTagName("tr");
    var sort_direction = $("#price_sort").attr("data-sort_direction") === "desc";
    $("table tbody tr").hide();
    var id;
    for (var i = 1; i < tr.length; i++) {
        if (num_results > max_num_rows) {
            tr[i].style.display = "none";
            continue;
        }
        if (sort_direction) {
            id = tr.length - i - 1;
        } else {
            id = i;
        }
        if (tr[i].dataset.filtered === "false") {
            num_results += 1;
            tr[i].style.display = "";
            $("table tbody").append($("#" + id));
        }
    }
    console.log(num_results);

}

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
    if (button.dataset.sort_direction === "asc") {
        button.dataset.sort_direction = "desc";
        button.innerHTML = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-arrow-down" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M8 1a.5.5 0 0 1 .5.5v11.793l3.146-3.147a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 .708-.708L7.5 13.293V1.5A.5.5 0 0 1 8 1z"/></svg>';
    } else {
        button.dataset.sort_direction = "asc";
        button.innerHTML = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-arrow-up" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M8 15a.5.5 0 0 0 .5-.5V2.707l3.146 3.147a.5.5 0 0 0 .708-.708l-4-4a.5.5 0 0 0-.708 0l-4 4a.5.5 0 1 0 .708.708L7.5 2.707V14.5a.5.5 0 0 0 .5.5z"/></svg>';
    }
    sort_table();
}

function search_filter(filter, td) {
    return (td.textContent || td.innerText).toUpperCase().indexOf(filter) > -1;
}

function stock_filter(active, td) {
    return !(active && (td.textContent || td.innerText) === "Out of stock");
}

function filter_table() {
    var store, text_color, link, item, stock, price, time, row, index;
    var filter_item = document.getElementById("search_form_item").value.toUpperCase();
    var filter_store = document.getElementById("search_form_store").value.toUpperCase();
    var filter_stock = document.getElementById("in_stock_check").classList.contains("active");
    var table = $("#myTable tbody");
    table.find("tr").hide();
    var num_results = 0;
    for (var i = 0; i < table_array.length; i++) {
        if (num_results >= max_num_rows) {
            break;
        }
        row = table_array[i];
        store = row[0];
        link = row[1];
        item = row[2];
        stock = row[3];
        price = row[4];
        if (stock === "Out of stock") {
            text_color = "text-danger";
        } else {
            text_color = "text-dark";
        }
        if (store.toUpperCase().indexOf(filter_store) === -1) {
            continue;
        }
        index = item.toUpperCase().indexOf(filter_item)
        if (index === -1) {
            continue;
        } else {
            item = item.slice(0, index) + "<b>" + item.slice(index, index + filter_item.length) + "</b>" + item.slice(index + filter_item.length);
        }
        if (filter_stock && stock === "Out of stock") {
            continue;
        }
        time = moment.unix(row[5]).fromNow();
        num_results += 1
        table.append(`<tr><td>${store}</td><td><a class='${text_color}' href='${link}' target='_blank'>${item}</a></td><td class='${text_color}'>${stock}</td><td>${price}</td><td>${time}</td></tr>`);
    }
    hidden_alert()
}

function filter_table_old() {
    var table = document.getElementById("myTable");
    var tr = table.getElementsByTagName("tr");
    var stock_check_active = document.getElementById("in_stock_check").classList.contains("active");
    var filter_item = document.getElementById("search_form_item").value.toUpperCase();
    var filter_store = document.getElementById("search_form_store").value.toUpperCase();
    var num_results = 0;

    var td_stock;
    var td_item;
    var td_store;
    for (var i = 0; i < tr.length; i++) {

        td_stock = tr[i].getElementsByTagName("td")[2];
        td_item = tr[i].getElementsByTagName("td")[1];
        td_store = tr[i].getElementsByTagName("td")[0];

        if (td_item && td_stock) {
            if (search_filter(filter_item, td_item) && stock_filter(stock_check_active, td_stock) && search_filter(filter_store, td_store)) {
                tr[i].dataset.filtered = "false";
                num_results += 1;
                if (num_results > max_num_rows) {
                    tr[i].style.display = "none";
                } else {
                    tr[i].style.display = "";
                }
            } else {
                tr[i].dataset.filtered = "true";
                tr[i].style.display = "none";
            }
        }
    }
    hidden_alert();
}
