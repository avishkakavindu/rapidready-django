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