var max_num_rows = 50;
var table_array = {{table}};
var stores_list = $("#stores_list");

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
    filter_table();
}

function filter_table() {
    var store, text_color, link, item, stock, price, time, row, index;
    var filter_item = document.getElementById("search_form_item").value.toUpperCase();
    var filter_stock = document.getElementById("in_stock_check").classList.contains("active");
    var table = $("#myTable tbody");
    table.find("tr").hide();
    var num_results = 0;
    var new_array = [];
    var stores = stores_list.find($("input:checked:not(#all_stores_check)")).map(function () {
        return $(this).attr('id');
    }).get();

    function price_sort(a, b) {
        return a[6] - b[6];
    }

    var sort_button = document.getElementById("price_sort");
    if (sort_button.dataset.sort_direction === "asc") {
        table_array.sort(price_sort).reverse();
    } else if (sort_button.dataset.sort_direction === "desc") {
        table_array.sort(price_sort);
    }
    for (var i = 0; i < table_array.length; i++) {
        if (num_results >= max_num_rows) {
            break;
        }
        row = table_array[i];
        store = row[0];
        item = row[2];
        stock = row[3];
        if (item.toUpperCase().indexOf(filter_item) === -1) {
            continue;
        }
        if (filter_stock && stock === "Out of stock") {
            continue;
        }
        if (stores.length !== 0 && !stores.includes(store)) {
            continue;
        }
        num_results += 1
        index = item.toUpperCase().indexOf(filter_item)
        item = item.slice(0, index) + "<b>" + item.slice(index, index + filter_item.length) + "</b>" + item.slice(index + filter_item.length);
        if (stock.toUpperCase() === "OUT OF STOCK") {
            text_color = "text-danger";
        } else {
            text_color = "text-dark";
        }
        price = row[4];
        time = moment.unix(row[5]).fromNow();
        table.append(`<tr><td>${store}</td><td><a class='${text_color}' href='${link}' target='_blank'>${item}</a></td><td class='${text_color}'>${stock}</td><td>${price}</td><td>${time}</td></tr>`);
    }


    hidden_alert()
}
$("#stores_list .dropdown-item").on('click', function (e) {
    e.stopPropagation();
    filter_table();
});
$("#all_stores_check").change(function (e) {
    var stores_list = $("#stores_list");
    var store_label = $("#store_label");
    store_label.addClass("text-secondary");
    if (this.checked) {
        store_label.text("None");
        stores_list.find("input").prop("checked", true);
    } else {
        store_label.text("All");
        stores_list.find("input").prop("checked", false);
    }
    filter_table();
});
