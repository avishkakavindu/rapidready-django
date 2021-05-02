// profile pic upload btn
$(".profile-pic-edit").click(function () {
    $("input[type='file']").trigger('click');


  });
// preview
id_profile_pic.onchange = function (event) {
    frame.src=URL.createObjectURL(event.target.files[0]);
}

// when edit button clicked
$(".editProfile").click(function(){
    $('#editProfile').addClass('d-none');
    $('#saveProfile').removeClass('d-none');
    $('#personalDetails').find('input').removeAttr('readonly');
});

// Retrieve individual order details # Click event handling
var order_links = $('#orders-list').find('.order-link');

for(let i=0; i < order_links.length; i++){
    order_links[i].addEventListener('click',function(event){
        event.preventDefault();
        let order_id = $(this).data('service');
        getOrderDetails(order_id);
    });
}

function getOrderDetails(order_id){

    let payload = {
      "url": "http://127.0.0.1:8000/order/${order_id}/",
      "method": "GET",
      "timeout": 0,
    };
    console.log(payload);
    $.ajax(payload).done(function (response) {
      console.log(response);
    });
}
