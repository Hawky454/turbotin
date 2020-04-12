function adjustHeight() {
    if (window.scrollY < 48 && getComputedStyle(document.getElementById("sub-header")).display !== "none") {
        document.getElementById("header").style = "box-shadow: none";
    } else {
        document.getElementById("header").style = "box-shadow: 0 2px 5px 0 rgba(0,0,0,0.16), 0 2px 10px 0 rgba(0,0,0,0.12)";
    }
}

window.onscroll = function() {
    adjustHeight();
};
window.onresize = function() {
    adjustHeight();
};