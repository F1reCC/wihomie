jQuery(document).ready(function($) {
    $("#query").autocomplete({
        source: "/search_auto/",
        select: function (event, ui) { //item selected
            AutoCompleteSelectHandler(event, ui)
        },
        minLength: 2,
    });
});
function AutoCompleteSelectHandler(event, ui)
{
    var selectedObj = ui.item;
}