// profile pic upload btn
$(".profile-pic-edit").click(function () {
    $("input[type='file']").trigger('click');


});
// preview
id_profile_pic.onchange = function (event) {
    frame.src = URL.createObjectURL(event.target.files[0]);
}

// when edit button clicked
$(".editProfile").click(function () {
    $('#editProfile').addClass('d-none');
    $('#saveProfile').removeClass('d-none');
    $('#personalDetails').find('input').removeAttr('readonly');
});

// Retrieve individual order details # Click event handling
var order_links = $('#orders-list').find('.order-link');

for (let i = 0; i < order_links.length; i++) {
    order_links[i].addEventListener('click', function (event) {
        event.preventDefault();
        let order_id = $(this).data('service');
        console.log('calling getOrderDetails');
        getOrderDetails(order_id);
    });
}

// Handles AJAX request to order retrieving endpoint
function getOrderDetails(order_id) {
    let payload = {
        "url": `http://127.0.0.1:8000/order/${order_id}/`,
        "method": "GET",
        "timeout": 0,
        "dataType": "json",
    };

    $.ajax(payload).done(function (response) {
        console.log(response);
        renderToModal(response);
    });
}

// Handles rendering the AJAX response to the modal
function renderToModal(payload) {
    $('#orderModal').find('.order_id').text(` #${payload.id}`);
    $('#orderModal').find('#created_on').after(` <span>${payload.created_on}</span>`);
    $('#orderModal').find('#summary_total').after(` <span>${payload.get_total}</span>`);
    $('#orderModal').find('#payment_method').after(` <span>${payload.payment_method}</span>`);
    $('#orderModal').find('#delivery_address').after(` <span>${payload.street}, ${payload.city}, ${payload.state}, ${payload.zipcode}</span>`);
    $('#orderModal').find('#contact_no').after(` <span>${payload.telephone}</span>`);
    payload.orderedservice_set.forEach(renderItems);

}

// Renders ordered items

function renderItems(item, index) {
    $('#orderModal').find('#order_summary tbody').append(`<tr>
                                                            <td scope="col" id="p_name">
                                                                <a href="{% url 'service' ${item.id} %}">
                                                                    ${item.service}
                                                                </a>
                                                            </td>
                                                            <td scope="col">${item.quantity}</td>
                                                            <td scope="col">$ ${item.unit_price}</td>
                                                            <td scope="col">${item.discount} off</td>
                                                            <td scope="col">${item.actual_price}</td>
                                                        </tr>`);
}