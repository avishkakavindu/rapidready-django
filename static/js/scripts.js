const url = window.location.href.split('/');
const protocol = url[0];
const domain = url[2];

// hide alert
$(function(){
    $("[data-hide]").on("click", function(){
        $("." + $(this).attr("data-hide")).removeClass('show');
    });
});

// service rating light up
$('.star-rating').each(function () {
    var rating = $(this).data('rating');

    for (let i = 1; i <= 5; i++) {
        if (i <= rating) {
            $(this).append(
                '<i class="fa fa-star" aria-hidden="true"></i>'
            );
        } else if (Math.floor(rating) === (i - 1) && Math.floor(rating) < rating) {
            $(this).append(
                '<i class="fa fa-star-half-o" aria-hidden="true"></i>'
            );
        } else {
            $(this).append(
                '<i class="fa fa-star-o" aria-hidden="true"></i>'
            );
        }
    }
});

// star rating system
$('.rate-me').mouseover(function () {

    $(this).prevAll().addBack().each(function () {
        $(this).removeClass('fa-star-o')
        $(this).addClass('fa-star')
        rating++

    })
    $(this).nextAll().each(function () {
        $(this).removeClass('fa-star')
        $(this).addClass('fa-star-o')
    })
    var rating = $('.rate-me.fa-star').length
    $('#id_rating').val(rating)
})

// Add quote
$('#getQuote button').click(function () {
        let desc = $('#quote_desc').val();
        let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        let payload = {
            "url": `${$(location).attr('protocol')}//127.0.0.1:8000/quote/create/`,
            "method": "POST",
            "data": {
                "csrfmiddlewaretoken": csrf_token,
                "desc": desc
            },
            "timeout": 0,
            "dataType": "json",
        };

        let alert = $('#quote_alert');

        $.ajax(payload).done(function (response) {
            alert.addClass('alert-success show');
            $('#getQuote form').trigger("reset");
            $('#getQuote').modal('toggle');
            alert.find('span').text('Quote recieved! Please be patient and wait for a email');
        }).fail(function (response){
            alert.addClass('alert-danger show');
            alert.find('span').text("Error! Invalid input");
        });
});

// Get cart item count
$('document').ready(function (){
    let payload = {
        "url": `${$(location).attr('protocol')}//127.0.0.1:8000/cart-item/`,
        "method": "GET",
        "timeout": 0,
        "dataType": "json",
    };
    callCartEndPoints(payload);
} );

// Add to cart from service page
$('#add-to-cart').click(function(){
    let service = $(this).data('service');
    let quantity = $('#service-quantity').val();
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    let payload = {
        "url": `${$(location).attr('protocol')}//127.0.0.1:8000/cart-item/`,
        "method": "POST",
        "timeout": 0,
        "dataType": "json",
        "data": {
            "csrfmiddlewaretoken": csrf_token,
            'service': service,
            'quantity': quantity
        }
    };
    callCartEndPoints(payload);
});

// call cart end points
function callCartEndPoints(payload){
    $.ajax(payload).done(function (response) {
        updateCartIcon(response['Item Count'])
    });
}

// update cart icon
function updateCartIcon(num_of_items){
    $('#cart-icon-num').text(num_of_items);
}
