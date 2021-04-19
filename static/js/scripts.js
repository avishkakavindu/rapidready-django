// service rating light up
$('.star-rating').each(function(){
    var rating = $(this).data('rating');

    for(let i=1 ; i<=5; i++){
        if(i<=rating){
            $(this).append(
                '<i class="fa fa-star" aria-hidden="true"></i>'
            );
        }
        else if(Math.floor(rating) === (i-1) && Math.floor(rating) < rating){
            $(this).append(
                '<i class="fa fa-star-half-o" aria-hidden="true"></i>'
            );
        }
        else{
            $(this).append(
                '<i class="fa fa-star-o" aria-hidden="true"></i>'
            );
        }
    }
});

// star rating system
$('.rate-me').mouseover(function(){

    $(this).prevAll().addBack().each(function(){
        $(this).removeClass('fa-star-o')
        $(this).addClass('fa-star')
        rating++

    })
    $(this).nextAll().each(function(){
        $(this).removeClass('fa-star')
        $(this).addClass('fa-star-o')
    })
    var rating = $('.rate-me.fa-star').length
    $('#id_rating').val(rating)
})
