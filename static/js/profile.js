const $orderModal = $('#orderModal');   // order detail model in profile page

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
const order_links = $('#orders-list').find('.order-link');

for (let i = 0; i < order_links.length; i++) {
    order_links[i].addEventListener('click', function (event) {
        event.preventDefault();
        let order_id = $(this).data('service');
        // console.log('calling getOrderDetails');
        getOrderDetails(order_id);
    });
}

// Handles AJAX request to order retrieving endpoint
function getOrderDetails(order_id) {
    let payload = {
        "url": `${protocol}//${domain}/order/${order_id}/`,
        "method": "GET",
        "timeout": 0,
        "dataType": "json",
    };

    $.ajax(payload).done(function (response) {
        // console.log(response);
        renderToModal(response);
    });
}

// Handles rendering the AJAX response to the modal
function renderToModal(payload) {
    $orderModal.find('.order_id').empty().text(` #${payload.id}`);
    $orderModal.find('#created_on').empty().text(`${payload.created_on}`);
    $orderModal.find('#summary_total').empty().text(`${payload.get_total}`);
    $orderModal.find('#payment_method').empty().text(`${payload.payment_method}`);
    $orderModal.find('#delivery_address').empty().text(`${payload.street}, ${payload.city}, ${payload.state}, ${payload.zipcode}`);
    $orderModal.find('#contact_no').empty().text(`${payload.telephone}`);
    $orderModal.find('#order_summary tbody').empty();
    payload.orderedservice_set.forEach(renderItems);
    $orderModal.find('#order_summary tbody').append(`
                                                        <tr>
                                                            <td colspan="4" style="font-size: 15px"><strong>Total</strong>
                                                            </td>
                                                            <td style="font-size: 15px"><strong>${payload.get_total}</strong></td>
                                                        </tr>
`);

}

// Renders ordered items
// * remove 8000 on deploy
function renderItems(item) {
    $orderModal.find('#order_summary tbody').append(`<tr>
                                                            <td scope="col" id="p_name">
                                                                <a href=${protocol + '://' + domain}/service/${item.id}/> 
                                                                    ${item.service}
                                                                </a>
                                                            </td>
                                                            <td scope="col">${item.quantity}</td>
                                                            <td scope="col">$ ${item.unit_price}</td>
                                                            <td scope="col">${item.discount}% off</td>
                                                            <td scope="col">${item.get_price_for_ordered_batch}</td>
                                                        </tr>`);
}