$(document).ready(function() {
    var set_currency = $("#currency_type").val();
    console.log(set_currency);
    convertCurrency(set_currency);
    currency_change(set_currency);
    var current = $("#current").val();
    var name = $("#currency_name").val();
    var sym = $("#currency_symbol").val();
    var name_with_sym = name.concat(" ", sym);
    $(".currency-text").html(name_with_sym);
    currency(current);
});

$(".country-drop span").click(function() {
    var countrySelect = $(this).text();
    $(".country-box").val(countrySelect);
});

$(document).ready(function() {

    var currency_type;

    $(".currency_selected").click(function() {
        currency_type = $(this).attr("name");
        convertCurrency(currency_type);
        currency_change(currency_type);
        //$("#currency_select_list").closest("form").submit();
    });


    $(".currency-drop span").click(function() {
        var currencySelect = $(this).text();
        $(".currency-text").html(currencySelect);
    });
    $(".country_search").click(function(e) {
        e.preventDefault();
        var country_name = $(this).attr("name");
        var patt1 = /\s/g;
        var result = patt1.test(country_name);
        if (result) {
            var name = country_name.split(" ");
            if (typeof currency_type === 'undefined') {
                window.location.href = "/all-deals/" + name[0] + "-" + name[1];
            } else {
                window.location.href = "/all-deals/" + name[0] + "-" + name[1] + "?utf8=?&currency=" + currency_type;
            }

        } else {

            if (typeof currency_type === 'undefined') {
                window.location.href = "/all-deals/" + country_name;
            } else {
                window.location.href = "/all-deals/" + country_name + "?utf8=?&currency=" + currency_type;
            }
        }
    });



});

function selectCurrency() {
    $("#currency_select_list").closest("form").submit();
}

function currency_change(a) {

    var slug = $("#slug").val();
    var selectedCurrencyValue = a;
    //alert(selectedCurrencyValue);
    if (selectedCurrencyValue != "undefined" && selectedCurrencyValue != null && selectedCurrencyValue != "") {
        var selectedCurrency = selectedCurrencyValue.split("-");
        //alert(selectedCurrency);
        if (selectedCurrency.length == 3) {
            if (selectedCurrency[0] == "AUD") {
                $('.currency_original').each(function() {
                    $(this).parent().find(".currency").first().html($(this).html());
                });
            } else {
                // Load exchange rates data via AJAX:
                $.ajax({
                    url: 'http://openexchangerates.org/api/latest.json?app_id=521c36e0271c463ca824efb550c061b9&base=AUD',
                    dataType: 'jsonp',
                    success: function(json) {
                        // Rates are in `json.rates`
                        // Base currency (AUD) is `json.base`
                        // UNIX Timestamp when rates were collected is in `json.timestamp`

                        // If you're using money.js, do this:
                        fx.rates = json.rates;
                        //alert(fx.rates);
                        fx.base = json.base;
                        $('.currency_original').each(function() {

                            var value = $(this).text().replace('$', '');
                            //alert(selectedCurrency[0]);
                            var price = fx.convert(value, { from: "AUD", to: selectedCurrency[0] });
                            //alert(price);
                            var currencyFormat = (selectedCurrency[2] == "false") ? "%s%v" : "%v%s";
                            //$(".currency").attr("text",price);
                            $(this).parent().find(".currency").first().html(accounting.formatMoney(price, { symbol: selectedCurrency[1], format: currencyFormat }));
                        });

                        $('.deal_was_price_original').each(function() {
                            var value = $(this).val().replace('$', '');
                            var price = fx.convert(value, { from: "AUD", to: selectedCurrency[0] });
                            var currencyFormat = (selectedCurrency[2] == "false") ? "%s%v" : "%v%s";

                            $(this).parent().find("#deal_was_price").first().val(accounting.formatMoney(price, { symbol: selectedCurrency[1], format: currencyFormat }));
                        });

                        $('.deal_now_price_original').each(function() {
                            var value = $(this).val().replace('$', '');
                            var price = fx.convert(value, { from: "AUD", to: selectedCurrency[0] });
                            var currencyFormat = (selectedCurrency[2] == "false") ? "%s%v" : "%v%s";

                            $(this).parent().find("#deal_now_price").first().val(accounting.formatMoney(price, { symbol: selectedCurrency[1], format: currencyFormat }));
                        });
                        $('.currency_input').each(function() {

                            var value = $(this).attr('currency_original').replace('$', '');
                            //alert(selectedCurrency[0]);
                            var price = fx.convert(value, { from: "AUD", to: selectedCurrency[0] });
                            //alert(price);
                            var currencyFormat = (selectedCurrency[2] == "false") ? "%s%v" : "%v%s";
                            //$(".currency").attr("text",price);
                            $(this).val(accounting.formatMoney(price, { symbol: selectedCurrency[1], format: currencyFormat }));
                        });
                        //alert("yes exicuted");
                        if (a == 'undefined') {

                            $.ajax({
                                url: "/deals/" + slug,
                                success: function(result) {

                                }
                            });
                            //alert("undifie++");
                            //window.location.href="/deals/"+slug;
                        } else {

                            $.ajax({
                                url: "/deals/" + slug + "?currency=" + a,
                                success: function(result) {

                                }
                            });
                            //alert("no");
                            //window.location.href="/deals/"+slug+ "?currency="+a;
                        }


                        if (document.getElementById("deal-slider")) {
                            update_data();
                        }
                    }
                });
            }
        }
    }


}

function currency(a) {


    var selectedCurrencyValue = a;
    //alert(selectedCurrencyValue);
    if (selectedCurrencyValue != "undefined" && selectedCurrencyValue != null && selectedCurrencyValue != "") {
        var selectedCurrency = selectedCurrencyValue.split("-");
        //alert(selectedCurrency);
        if (selectedCurrency.length == 3) {
            if (selectedCurrency[0] == "AUD") {
                $('.currency_original').each(function() {
                    $(this).parent().find(".currency").first().html($(this).html());
                });
            } else {
                // Load exchange rates data via AJAX:
                $.ajax({
                    url: 'http://openexchangerates.org/api/latest.json?app_id=521c36e0271c463ca824efb550c061b9&base=AUD',
                    dataType: 'jsonp',
                    success: function(json) {
                        // Rates are in `json.rates`
                        // Base currency (AUD) is `json.base`
                        // UNIX Timestamp when rates were collected is in `json.timestamp`

                        // If you're using money.js, do this:
                        fx.rates = json.rates;
                        //alert(fx.rates);
                        fx.base = json.base;
                        $('.currency_original').each(function() {

                            var value = $(this).text().replace('$', '');
                            //alert(selectedCurrency[0]);
                            var price = fx.convert(value, { from: "AUD", to: selectedCurrency[0] });
                            //alert(price);
                            var currencyFormat = (selectedCurrency[2] == "false") ? "%s%v" : "%v%s";
                            //$(".currency").attr("text",price);
                            $(this).parent().find(".currency").first().html(accounting.formatMoney(price, { symbol: selectedCurrency[1], format: currencyFormat }));
                        });

                        $('.deal_was_price_original').each(function() {
                            var value = $(this).val().replace('$', '');
                            var price = fx.convert(value, { from: "AUD", to: selectedCurrency[0] });
                            var currencyFormat = (selectedCurrency[2] == "false") ? "%s%v" : "%v%s";

                            $(this).parent().find("#deal_was_price").first().val(accounting.formatMoney(price, { symbol: selectedCurrency[1], format: currencyFormat }));
                        });

                        $('.deal_now_price_original').each(function() {
                            var value = $(this).val().replace('$', '');
                            var price = fx.convert(value, { from: "AUD", to: selectedCurrency[0] });
                            var currencyFormat = (selectedCurrency[2] == "false") ? "%s%v" : "%v%s";

                            $(this).parent().find("#deal_now_price").first().val(accounting.formatMoney(price, { symbol: selectedCurrency[1], format: currencyFormat }));
                        });

                        console.log("b");
                        $('.currency_input').each(function() {
                            console.log("b");

                            var value = $(this).attr('currency_original').replace('$', '');
                            //alert(selectedCurrency[0]);
                            var price = fx.convert(value, { from: "AUD", to: selectedCurrency[0] });
                            //alert(price);
                            var currencyFormat = (selectedCurrency[2] == "false") ? "%s%v" : "%v%s";
                            //$(".currency").attr("text",price);
                            $(this).val(accounting.formatMoney(price, { symbol: selectedCurrency[1], format: currencyFormat }));
                        });



                        if (document.getElementById("deal-slider")) {
                            update_data();
                        }
                    }
                });
            }
        }
    }
}
$(document).ready(function() {

    convertCurrency();
});

function selectCurrency() {
    $("#currency_select_list").closest("form").submit();
    //convertCurrency();
}
$(document).ready(function() {
    if ($.cookie('TAD_Lead') == null) {
        //if (!<%=user_signed_in?%>)
        $("#subscibeNewsletter").modal();
        $('#subscibeNewsletter').css('display', '-webkit-box');
        $('#subscibeNewsletter').css('display', '-moz-box');
        $('#subscibeNewsletter').css('display', '-ms-flexbox');
        $('#subscibeNewsletter').css('display', '-webkit-flex');
        $('#subscibeNewsletter').css('display', 'flex');
        $.cookie("TAD_Lead", "1", { path: '/' });
    }
    $('#news-letter-modal').on('show.bs.modal', function(e) {
        $('#subscibeNewsletter').modal('hide');
    })
});

function convertCurrency() {
    var selectedCurrencyValue = $("#currency_select_list").val();
    if (selectedCurrencyValue != "undefined" && selectedCurrencyValue != null && selectedCurrencyValue != "") {
        var selectedCurrency = selectedCurrencyValue.split("-");

        if (selectedCurrency.length == 3) {
            if (selectedCurrency[0] == "AUD") {
                $('.currency_original').each(function() {
                    $(this).parent().find(".currency").first().html($(this).html());
                });
            } else {
                // Load exchange rates data via AJAX:
                $.ajax({
                    url: 'http://openexchangerates.org/api/latest.json?app_id=521c36e0271c463ca824efb550c061b9&base=AUD',
                    dataType: 'jsonp',
                    success: function(json) {
                        // Rates are in `json.rates`
                        // Base currency (AUD) is `json.base`
                        // UNIX Timestamp when rates were collected is in `json.timestamp`

                        // If you're using money.js, do this:
                        fx.rates = json.rates;
                        fx.base = json.base;
                        $('.currency_original').each(function() {
                            var value = $(this).text().replace('$', '');
                            var price = fx.convert(value, { from: "AUD", to: selectedCurrency[0] });
                            var currencyFormat = (selectedCurrency[2] == "false") ? "%s%v" : "%v%s";

                            $(this).parent().find(".currency").first().html(accounting.formatMoney(price, { symbol: selectedCurrency[1], format: currencyFormat }));
                        });

                        $('.deal_was_price_original').each(function() {
                            var value = $(this).val().replace('$', '');
                            var price = fx.convert(value, { from: "AUD", to: selectedCurrency[0] });
                            var currencyFormat = (selectedCurrency[2] == "false") ? "%s%v" : "%v%s";

                            $(this).parent().find("#deal_was_price").first().val(accounting.formatMoney(price, { symbol: selectedCurrency[1], format: currencyFormat }));
                        });

                        $('.deal_now_price_original').each(function() {
                            var value = $(this).val().replace('$', '');
                            var price = fx.convert(value, { from: "AUD", to: selectedCurrency[0] });
                            var currencyFormat = (selectedCurrency[2] == "false") ? "%s%v" : "%v%s";

                            $(this).parent().find("#deal_now_price").first().val(accounting.formatMoney(price, { symbol: selectedCurrency[1], format: currencyFormat }));
                        });

                        console.log("A");
                        $('.currency_input').each(function() {
                            console.log("a");
                            var value = $(this).attr('currency_original').replace('$', '');
                            //alert(selectedCurrency[0]);
                            var price = fx.convert(value, { from: "AUD", to: selectedCurrency[0] });
                            //alert(price);
                            var currencyFormat = (selectedCurrency[2] == "false") ? "%s%v" : "%v%s";
                            //$(".currency").attr("text",price);
                            $(this).val(accounting.formatMoney(price, { symbol: selectedCurrency[1], format: currencyFormat }));
                        });

                        if (document.getElementById("deal-slider")) {
                            update_data();
                        }
                    }
                });
            }
        }
    }
}
