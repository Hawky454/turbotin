var max_num_rows = 50;
var table_array = {{table}};

// function show_more() {
//     max_num_rows += 100;
//     filter_table();
//     hidden_alert();
// }

// function hidden_alert() {
//     var alert_container = $("#alert_container");
//     if ($('#myTable tr:visible').length > max_num_rows) {
//         $("#alert").text("Only showing first " + max_num_rows + " rows");
//         alert_container.show();
//     } else {
//         alert_container.hide();
//     }
// }

// function toggle_stock() {
//     var check_box = document.getElementById("in_stock_check");
//     if (check_box.classList.contains("active")) {
//         check_box.classList.remove("active");
//     } else {
//         check_box.classList.add("active");
//     }
//     filter_table();
// }

// function toggle_sort() {
//     var button = document.getElementById("price_sort");
//     if (button.dataset.sort_direction === "asc") {
//         button.dataset.sort_direction = "desc";
//         button.innerHTML = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-arrow-down" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M8 1a.5.5 0 0 1 .5.5v11.793l3.146-3.147a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 .708-.708L7.5 13.293V1.5A.5.5 0 0 1 8 1z"/></svg>';
//     } else {
//         button.dataset.sort_direction = "asc";
//         button.innerHTML = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-arrow-up" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M8 15a.5.5 0 0 0 .5-.5V2.707l3.146 3.147a.5.5 0 0 0 .708-.708l-4-4a.5.5 0 0 0-.708 0l-4 4a.5.5 0 1 0 .708.708L7.5 2.707V14.5a.5.5 0 0 0 .5.5z"/></svg>';
//     }
//     filter_table();
// }

function get_filtered_dict(allowed_stores = [], filter_stock = false, item_filter = "", sort) {

    function price_sort(a, b) {
        return a[6] - b[6];
    }

    if (typeof sort !== 'undefined') {
        table_array.sort(price_sort);
        if (sort === "desc")
            table_array.reverse();
    }

    var row, store, link, item, stock, price, time, index;
    var table_dict = [];
    var num_results = 0;
    for (var i = 0; i < table_array.length; i++) {

        if (num_results >= max_num_rows)
            break;

        row = table_array[i];
        store = row[0];
        link = row[1];
        item = row[2];
        stock = row[3];

        if (item.toUpperCase().indexOf(item_filter) === -1)
            continue;
        if (filter_stock && stock === "Out of stock")
            continue;
        if (allowed_stores.length !== 0 && !allowed_stores.includes(store))
            continue;

        num_results += 1;
        index = item.toUpperCase().indexOf(item_filter);
        item = item.slice(0, index) + "<b>" + item.slice(index, index + item_filter.length) + "</b>" + item.slice(index + item_filter.length);
        price = row[4];
        time = moment.unix(row[5]).fromNow();
        table_dict.push({"store": store, "link": link, "item": item, "stock": stock, "price": price, "time": time});
    }
    return table_dict;
}
// $("#stores_list .dropdown-item").on('click', function (e) {
//     e.stopPropagation();
//     filter_table();
// });
var stores_checkboxes = [];
for (let i = 1; i < document.getElementById("store_dropdown").childElementCount - 1; i++)
    stores_checkboxes.push(document.getElementById("store_dropdown" + i.toString()))

function filter_table() {
    var allowed_stores = [];
    for (var store of stores_checkboxes) {
        if (store.checked)
            allowed_stores.push(store.nextElementSibling.innerText)
    }
    var table_dict = get_filtered_dict(allowed_stores)
    var table = document.getElementById("table_body")
    table.innerHTML = null;
    for (var row of table_dict) {
        row.item = `<a class="link-secondary" href="${row.link}" target="_blank">${row.item}</a>`;
        delete row.link;
        var new_row = document.getElementById("row_template").content.cloneNode(true);
        for (var key in row) {
            var cell = new_row.querySelector("#" + key);
            cell.innerHTML = row[key]
            cell.removeAttribute("id");
        }
        table.append(new_row)
    }
    document.getElementById("store_dropdown").addEventListener("click", function (ev) {
        ev.stopPropagation()
    });
}
document.getElementById("store_dropdown0").addEventListener("change", filter_table, false);
for (var store of stores_checkboxes) {
    store.addEventListener("change", filter_table, false);
}

filter_table();