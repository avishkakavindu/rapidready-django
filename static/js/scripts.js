const url = window.location.href.split('/');
const protocol = url[0];
const domain = url[2];

// hide alert
$(function () {
    $("[data-hide]").on("click", function () {
        $("." + $(this).attr("data-hide")).removeClass('show');
    });
    starrateme();
});

// service rating light up
function starrateme() {
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
}

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
        "url": `${$(location).attr('protocol')}//${domain}/quote/create/`,
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
    }).fail(function (response) {
        alert.addClass('alert-danger show');
        alert.find('span').text("Error! Invalid input");
    });
});

// Get cart item count
$('document').ready(function () {
    let payload = {
        "url": `${$(location).attr('protocol')}//${domain}/cart-item/`,
        "method": "GET",
        "timeout": 0,
        "dataType": "json",
    };
    callCartEndPoints(payload);
});

// Add to cart from service page
$('#add-to-cart').click(function () {
    let service = $(this).data('service');
    let quantity = $('#service-quantity').val();
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    let payload = {
        "url": `${$(location).attr('protocol')}//${domain}/cart-item/`,
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
function callCartEndPoints(payload) {
    $.ajax(payload).done(function (response) {
        updateCartIcon(response['Item Count'])
    });
}

// update cart icon
function updateCartIcon(num_of_items) {
    $('#cart-icon-num').text(num_of_items);
}

// update cart prices on quantity change
$('.update-quantity').change(function () {
    let service = $(this).data('service');
    let quantity = $(this).val();
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    let payload = {
        "url": `${$(location).attr('protocol')}//${domain}/cart-detail/`,
        "method": "PUT",
        "timeout": 0,
        "headers": {
            "Content-Type": "application/json",
            "X-CSRFTOKEN": csrftoken
        },
        "data": JSON.stringify({"cartitem_set": [{"service": service, "quantity": quantity}]}),
    };

    $.ajax(payload).done(function (response) {
        for (let i = 0; i < response.cartitem_set.length; i++) {
            let cartitem = response.cartitem_set[i];
            if (cartitem.service === service) {
                $(`#cost-${cartitem.id}`).text(cartitem.get_total_for_item);
                $('#cart-total').text(response.get_cart_total);
                break;
            }
        }

    });


});

// remove item  from cart
$('.delete-item').click(function () {
    let item = $(this).data('item');
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    $(this).parent().parent().remove();

    let payload = {
        "url": `${$(location).attr('protocol')}//${domain}/cart-item/${item}/`,
        "method": "DELETE",
        "timeout": 0,
        "headers": {
            "Content-Type": "application/json",
            "X-CSRFTOKEN": csrftoken
        },
    };

    let alert = $('#quote_alert');

    $.ajax(payload).done(function (response) {
        alert.addClass('alert-danger show');
        alert.find('span').text('Item removed!');
        $('#cart-total').text(response['total']);
    });
});


$('#searchIcon').click(function () {
    let keyword = $('#searchBox').val();
    console.log('keyword: ', keyword);


    let payload = {
        "url": `${$(location).attr('protocol')}//${domain}/search/?search=${keyword}`,
        "method": "GET",
        "timeout": 0,
        "headers": {
            "Content-Type": "application/json"
        },
    };
    console.log(payload);
    $.ajax(payload).done(function (response) {
        console.log(response);
        response.forEach(renderSearchResult);
    });
});

// renders search results into modal
function renderSearchResult(result, index) {
    const search_modal = $('#searchModal').find('.modal-body');


    search_modal.append(
        `
        <div class="card mb-3 border" style="max-width: 100%;">
            <div class="row g-0">
                <div class="col-md-4">
                    <img src="${result['image']}" class="img-fluid rounded-start"
                         alt="service name">
                </div>
                <div class="col-md-8">
                    <div class="card-body">
                        <h5 class="card-title">${result['service']}</h5>
                        <p class="card-text">
                            ${result['desc']}
                        </p>
    
                        <div class="pricing">
                            <p>
                                <span>Price:</span>
                                    <span class="price-actual">
                                        ${result['price']}
                                    </span>         
                            </p>
                            <div class="row">
                                <a href="/service/${result['id']}" type="button"
                                    class="btn btn-outline-primary update-cart"
                                        data-action="add-serving"
                                        data-service="{{ service.id }}">
                                    <i class="fa fa-shopping-cart" aria-hidden="true"></i>
                                        <span> Shop Now</span>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `);

}
