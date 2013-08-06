function relationOnChange(el) {
    var effect = el.val();
    var map = el.data('map');
    var f1 = el.data('f1');
    var f2 = el.data('f2');

    $.post(
        "/map/change-factor",
        {
            map: map,
            f1: f1,
            f2: f2,
            effect: effect
        },
        function (data) {}
    );
}

function initRalationGrid() {
    $(".relation-effect").change(function (event) {
        relationOnChange($(this));
    });
}

$(document).ready(function () {
    initRalationGrid();
});