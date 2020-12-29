var brands = {{brands}};
var brand_search_list = [];
for (let brand of brands)
    brand_search_list.push({"link": `javascript:brand_clicked('${brand}')`, "text": brand});
var blends = {{blends}};

var brand_input = document.getElementById("brand_search_input");
var blend_input = document.getElementById("blend_search_input");
var invalid_input = document.getElementById("invalid_input");
function brand_clicked(brand) {
    brand_input.value = brand;
    blend_input.disabled = false;
    update_blends();
}
function blend_clicked(blend) {
    blend_input.value = blend;
    update_blends();
}
function update_blends() {
    var brand = brand_input.value;
    if (!brands.includes(brand))
        return false;
    var blend_search_list = [];
    for (let blend of blends[brand])
        blend_search_list.push({"link": `javascript:blend_clicked('${blend}')`, "text": blend})
    update_search("blend_search", blend_search_list, new bootstrap.Dropdown(blend_input));
    invalid_input.classList.add("d-none");
}
brand_input.addEventListener("input", function () {
    update_search("brand_search", brand_search_list, new bootstrap.Dropdown(brand_input));
    blend_input.disabled = !brands.includes(brand_input.value);
    if (brands.includes(brand_input.value)) {
        update_blends();
    } else {
        blend_input.value = "";
    }
    invalid_input.classList.add("d-none");
});
update_search("brand_search", brand_search_list, new bootstrap.Dropdown(brand_input));
blend_input.disabled = true;
blend_input.addEventListener("input", update_blends);
var show_stores_el = document.getElementById("show_stores")
show_stores_el.addEventListener("change", function () {
    show_stores_el.parentElement.classList.add("d-none");
    document.getElementById("stores_container").classList.remove("d-none");
    invalid_input.classList.add("d-none");
});

document.getElementById("submit").addEventListener("click", function () {
    var brand = brand_input.value;
    var blend = blend_input.value;
    var stores_el = document.getElementById("stores_container").getElementsByClassName("form-check");
    var stores = [];
    for (var i = 1; i < stores_el.length; i++) {
        if (stores_el[i].firstElementChild.checked)
            stores.push(stores_el[i].innerText.trim());
    }
    stores = JSON.stringify(stores)
    var max_price = document.getElementById("max_price_val").value;
    $.post("/email_updates/add_notification", {
        brand: brand,
        blend: blend,
        stores: stores,
        max_price: max_price
    }).done(function (data) {
        console.log(data);
        data = JSON.parse(data);
        if (data["failed"]) {
            invalid_input.innerText = data["what"];
            invalid_input.classList.remove("d-none");
        } else {
            location.reload();
        }
    });
});
function remove(i) {
    $.post("/email_updates/remove_notification", {
        index: i
    }).done(function (data) {
        if (!data["failed"])
            location.reload();
    });

};

function check_for_input() {
    var brand = "{{ brand }}";
    var blend = "{{ blend }}";
    if (brands.includes(brand) && blends[brand].includes(blend)) {
        brand_input.value = brand;
        blend_input.value = blend;
        blend_input.disabled = !brands.includes(brand_input.value);
        update_search("brand_search", brand_search_list, new bootstrap.Dropdown(brand_input));
        update_blends()
    }
}
check_for_input();