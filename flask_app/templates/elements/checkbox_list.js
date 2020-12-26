function update_checks(id, count) {
    var label = document.getElementById(id + "0")
    var checked;
    if (label.checked) {
        label.nextElementSibling.innerText = "None";
        checked = true;
    } else {
        label.nextElementSibling.innerText = "All";
        checked = false;
    }
    for (let i = 1; i < count; i++)
        document.getElementById(id + i.toString()).checked = checked;
}
function update_label(id, count) {
    var label = document.getElementById(id + "0")
    var num_checked = 0;
    for (let i = 1; i < count; i++) {
        if (document.getElementById(id + i.toString()).checked)
            num_checked++
    }

    if (num_checked === 0) {
        label.indeterminate = false;
        label.checked = false;
    } else if (num_checked === count - 1) {
        label.indeterminate = false;
        label.checked = true;
    } else {
        label.indeterminate = true;
    }

}