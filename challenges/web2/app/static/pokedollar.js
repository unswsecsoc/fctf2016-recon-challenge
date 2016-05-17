function pokeToAussie(val) {
    return (parseInt(val) * 0.42)
}

function AussieToPoke(val) {
    return (parseInt(val) / 0.42)
}

function convert(val, a, b){
    return fx(parseInt(val)).from(String(a)).to(String(b));
}

function changeEverything(old_currency, old_sym, new_currency, new_sym, first_time) {
    var i = 0;
    $(".price").each(function() {
        var newprice = convert(pokeToAussie($(this).text()), 'AUD', new_currency);
        if (i == 0) {
        $(this).parent().find(".price-sym").first().html(new_sym);i = 1;} else {
        $(this).parent().find(".price-sym").first().text(new_sym);}
        $(this).text(Math.round(newprice * 100) / 100);
    });
}

$(document).ready(function() {
    var currency = $("#currency_type").val();
    var current = $("#current").val();
    var name = $("#currency_name").val();
    var sym = $("#currency_symbol").val();
    var name_with_sym = name.concat(" ", sym);

    $(".currency-text").html(name_with_sym);
    if (name != 'PKD') {
        changeEverything(name, sym, name, sym, true);
    }


})

$(document).ready(function() {
    $(".currency_selected").click(function() {
        ct = $(this).attr("name").split("-");
        var new_currency = ct[0];
        var new_sym = ct[1]

        if (new_currency == name){
            return;
        }
        var loc = window.location.href;
        var newloc = $(this).attr('name');

        if (loc.indexOf("currency") > 0) {
            var newText = loc.replace(/(currency=).*$/,'$1' + newloc);
        } else {
            var newText = loc + "?currency=" + newloc;
        }

        window.location.href = newText;

        // changeEverything(new_currency, new_sym, false);

    });
});
