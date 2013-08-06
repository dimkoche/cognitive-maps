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

function koefOnChange(el) {
    var koef = el.val();
    var map = el.data('map');
    var f = el.data('f');

    $.post(
        "/map/change-koef",
        {
            map: map,
            f: f,
            koef: koef
        },
        function (data) {}
    );
}

function initRelationGrid() {
    $(".relation-effect").change(function (event) {
        relationOnChange($(this));
    });
    $(".factor-koef").change(function (event) {
        koefOnChange($(this));
    });
}

$(document).ready(function () {
    initRelationGrid();
});