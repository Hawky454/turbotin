var brands = {{brands}};
var blends = {{blends}};
var lowercase_brands = [];
for (var i = 0; i < brands.length; i++) {
    lowercase_brands.push(brands[i].toLowerCase());
}
function complete_element(element, self) {
    document.getElementById(element).value = self.innerText;
    $('#' + element).keyup();
}
var invalidInput = $("#invalid_input")
function filter_allowed(input_element_id, results_element_id, allowed_inputs) {
    var results_element = document.getElementById(results_element_id);
    var input_element = $("#" + input_element_id)
    var input_alert = $("#invalid_input");

    function hide_results() {
        results_element.classList.add("p-0", "m-0", "border-0");
        input_element.removeClass("border-danger");
        input_alert.hide();
    }

    var query = document.getElementById(input_element_id).value.toLowerCase();

    if (query === "") {
        results_element.innerHTML = "";
        hide_results();
        return;
    }
    var new_inner_html = "";
    var results = 0;

    for (var i = 0; i < allowed_inputs.length; i++) {
        if (allowed_inputs[i].toLowerCase() === query) {
            results_element.innerHTML = "";
            hide_results();
            return;
        }
        var index = allowed_inputs[i].toLowerCase().indexOf(query);
        if (index > -1) {
            var txt = allowed_inputs[i];
            txt = txt.slice(0, index) + "<b>" + txt.slice(index, index + query.length) + "</b>" + txt.slice(index + query.length);
            new_inner_html += "<a class='dropdown-item' href='#' onclick='complete_element(\"" + input_element_id + "\",this);return false'>" + txt + "</a>";
            results += 1
            if (results >= 10) {
                break;
            }
        }
    }
    if (new_inner_html !== "") {
        results_element.classList.remove("p-0", "m-0", "border-0");
        input_element.removeClass("border-danger");
        input_alert.hide();
        if (input_element.is(':focus') && !$("#" + results_element.id).hasClass("show")) {
            input_element.trigger("click");
        }
    } else {
        input_element.addClass("border-danger");
        results_element.classList.add("p-0", "m-0", "border-0");
    }
    results_element.innerHTML = new_inner_html;
    return true;
}


function brand_input() {
    filter_allowed("brand_input", "brand_results", brands);
    var blend_input = $("#blend_input");
    if (lowercase_brands.includes(document.getElementById("brand_input").value.toLowerCase())) {
        blend_input.prop("disabled", false);
        console.log("not disabled")
    } else {
        blend_input.prop("disabled", true);

        blend_input.val("");
    }
    invalidInput.hide();
}

function blend_input() {
    var brand = document.getElementById("brand_input").value;
    if (!lowercase_brands.includes(brand.toLowerCase())) {
        $("#blend_input").prop("disabled", true);
        brand_input()
        return;
    }
    filter_allowed("blend_input", "blend_results", blends[brand]);
    invalidInput.hide();
}
var all_stores_check = $("#all_stores_check");
all_stores_check.change(function () {
    var stores_list = $("#stores_list");
    var store_label = $("#store_label");
    store_label.addClass("text-secondary");
    if (store_label.text() === "Only specific stores") {
        all_stores_check.prop("checked", false);
        stores_list.slideDown("slow");
    }
    if (this.checked) {
        store_label.text("None");
        stores_list.find("input").prop("checked", true);
    } else {
        store_label.text("All");
        stores_list.find("input").prop("checked", false);
    }
    invalidInput.hide();
});
$("#stores_list").find("input").change(function () {
    var stores_list = $("#stores_list");
    var all_stores_check = $("#all_stores_check");

    var num_checked = stores_list.find($("input:checked")).length;
    var num_unchecked = stores_list.find($("input:not(:checked)")).length;
    var num_checkbox = stores_list.find("input").length;

    if ((num_checked !== num_checkbox) && (num_unchecked !== num_checkbox)) {
        all_stores_check.prop('indeterminate', true);
    } else {
        all_stores_check.prop('indeterminate', false);
        if (num_checked === num_checkbox) {
            all_stores_check.prop('checked', true);
        } else if (num_unchecked === num_checkbox) {
            all_stores_check.prop('checked', false);
        }
    }
    invalidInput.hide();
});
$("#submit").on("click", function () {
    var brand = $("#brand_input").val();
    var blend = $("#blend_input").val();

    var stores = JSON.stringify($("#stores_list").find($("input:checked:not(#all_stores_check)")).map(function () {
        return $(this).next().text();
    }).get());


    var max_price = $("#max_price_val").val();

    console.log({
        brand: brand,
        blend: blend,
        stores: stores,
        max_price: max_price
    });
    $.post("/email_updates/add_notification", {
        brand: brand,
        blend: blend,
        stores: stores,
        max_price: max_price
    }).done(function (data) {
        console.log(data);
        data = JSON.parse(data);
        if (data["failed"]) {
            invalidInput.text(data["what"] + " is invalid.");
            invalidInput.show();
        }
    });

});