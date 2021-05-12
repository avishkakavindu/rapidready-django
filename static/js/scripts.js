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