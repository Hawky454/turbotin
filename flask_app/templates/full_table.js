var max_num_rows = 50;
var table_array = {{table}};

function toggle_sort() {
    var button = document.getElementById("price_sort");
    var down_up_el = document.getElementById("price_sort_down_up");
    var down_el = document.getElementById("price_sort_down");
    var up_el = document.getElementById("price_sort_up");
    down_up_el.classList.add("d-none");
    down_el.classList.add("d-none");
    up_el.classList.add("d-none");
    if (button.dataset.sort_direction === "asc") {
        button.dataset.sort_direction = "desc";
        down_el.classList.remove("d-none")
    } else {
        button.dataset.sort_direction = "asc";
        up_el.classList.remove("d-none")
    }
    filter_table();
}

function get_filtered_dict(allowed_stores = [], filter_stock = false, item_filter = "", sort = "") {

    function price_sort(a, b) {
        return a[6] - b[6];
    }

    if (sort !== "") {
        table_array.sort(price_sort);
        if (sort === "desc")
            table_array.reverse();
    }

    var row, store, link, item, stock, price, time, index;
    var table_dict = [];
    var num_results = 0;
    for (var i = 0; i < table_array.length; i++) {

        if (num_results >= max_num_rows + 1)
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
        table_dict.push({
            "store": store,
            "link": link,
            "item": item,
            "stock": stock,
            "price": price,
            "time": time,
            "id": row[7]
        });
    }
    return table_dict;
}

var stores_checkboxes = [];
for (let i = 1; i < document.getElementById("store_dropdown").childElementCount - 1; i++)
    stores_checkboxes.push(document.getElementById("store_dropdown" + i.toString()))
var search_element = document.getElementById("item_search_input");
search_element.addEventListener("keyup", filter_table);

function filter_table() {
    var allowed_stores = [];
    for (var store of stores_checkboxes) {
        if (store.checked)
            allowed_stores.push(store.nextElementSibling.innerText.trim());
    }
    var item_filter = search_element.value.toUpperCase();
    var filter_stock = document.getElementById("in_stock").checked;
    var sort = document.getElementById("price_sort").dataset.sort_direction;

    var table_dict = get_filtered_dict(allowed_stores, filter_stock, item_filter, sort);
    var table = document.getElementById("table_body");
    table.innerHTML = null;
    for (var row of table_dict) {
        var color = "link-secondary"
        if (row.stock === "Out of stock")
            color = "link-danger"
        row.item = `<a class="${color}" href="${row.link}" target="_blank">${row.item}</a>`;
        delete row.link;
        var new_row = document.getElementById("row_template").content.cloneNode(true);
        new_row.querySelector("#price").firstElementChild.href = "/individual_blends/" + row.id;
        delete row.id;
        for (var key in row) {
            var cell = new_row.querySelector("#" + key);
            cell.innerHTML += row[key];
            cell.removeAttribute("id");
        }
        table.append(new_row)
    }
    under_table(table_dict.length === 0, table_dict.length >= max_num_rows);
    document.getElementById("store_dropdown").addEventListener("click", function (ev) {
        ev.stopPropagation()
    });
}
function under_table(empty, overfull) {
    var too_many_el = document.getElementById("too_many_matches");
    var no_el = document.getElementById("no_matches");
    if (empty) {
        no_el.classList.remove("d-none");
    } else {
        no_el.classList.add("d-none");
    }
    if (overfull) {
        too_many_el.classList.remove("d-none");
        document.getElementById("too_many_matches_alert").innerText = `Only showing the first ${max_num_rows} rows`;
    } else {
        too_many_el.classList.add("d-none");
    }

}
document.getElementById("store_dropdown0").addEventListener("change", filter_table, false);
for (var store of stores_checkboxes) {
    store.addEventListener("change", filter_table, false);
}
document.getElementById("show_more").addEventListener("click", function () {
    max_num_rows += 100;
    filter_table();
});
document.getElementById("in_stock").addEventListener("change", filter_table);
document.getElementById("price_sort").addEventListener("click", toggle_sort);

filter_table();