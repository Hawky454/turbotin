var brands = {{brands}};
var blends = {{blends}};
var lowercase_brands = [];
for (var i = 0; i < brands.length; i++) {
    lowercase_brands.push(brands[i].toLowerCase());
}

function complete_element(element, self) {
    document.getElementById(element).value = self.innerText;
    $('#'+element).keyup();
}

function filter_allowed(input_element, results_element, allowed_inputs) {
    results_element = document.getElementById(results_element);
    function hide_results() {
        results_element.classList.add("p-0", "m-0", "border-0");
        $("#"+input_element).removeClass("border-danger");
    }
    var query = document.getElementById(input_element).value.toLowerCase();

    if (query == ""){
        results_element.innerHTML = "";
        hide_results();
        return;
    }
    var new_inner_html = "";
    var results = 0;

    for (var i = 0; i < allowed_inputs.length; i++) {
        if (allowed_inputs[i].toLowerCase() == query) {
            results_element.innerHTML = "";
            hide_results();
            return;
        }
        var index = allowed_inputs[i].toLowerCase().indexOf(query);
        if (index > -1) {
            var txt = allowed_inputs[i];
            txt = txt.slice(0, index) + "<b>" + txt.slice(index, index+query.length) + "</b>" +txt.slice(index+query.length);
            new_inner_html += "<a class='dropdown-item' href='#' onclick='complete_element(\""+input_element+"\",this);return false'>"+txt+"</a>";
            results += 1
            if (results >= 10) { break; }
        }
    }
    if (new_inner_html != "") {
        results_element.classList.remove("p-0", "m-0", "border-0");
        $("#"+input_element).removeClass("border-danger");
        if ($("#"+input_element).is(':focus') && !$("#"+results_element.id).hasClass("show")) {
            $("#"+input_element).trigger("click");
        }
    } else {
        $("#"+input_element).addClass("border-danger");
        results_element.classList.add("p-0", "m-0", "border-0");
    }
    results_element.innerHTML = new_inner_html;
    return true;
}

function brand_input() {
    filter_allowed("brand_input", "brand_results", brands);
    if (lowercase_brands.includes(document.getElementById("brand_input").value.toLowerCase())) {
        $("#blend_input").prop( "disabled", false );
    } else {
        $("#blend_input").prop( "disabled", true );
        $("#blend_input").val("");
    }
}

function blend_input() {
    var brand = document.getElementById("brand_input").value;
    if (!lowercase_brands.includes(brand.toLowerCase())) {
        $("#blend_input").prop( "disabled", true );
        brand_input()
        return;
    }
    filter_allowed("blend_input", "blend_results", blends[brand]);


}