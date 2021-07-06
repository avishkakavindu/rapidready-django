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

// Review individual delivered orders
const order_rev_links = $('#orders-list').find('.review-order');

for (let i = 0; i < order_rev_links.length; i++) {
    order_rev_links[i].addEventListener('click', function (event) {
        event.preventDefault();
        let order_id = $(this).data('service');
        $('#id_id').val(order_id);
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
    $orderModal.find('#order_status').empty().append(getOrderStatus(payload.status));
    $orderModal.find('#created_on').empty().text(`${payload.created_on}`);
    $orderModal.find('#summary_total').empty().text(`${payload.get_total}`);
    $orderModal.find('#payment_method').empty().text(`${payload.payment_method}`);
    $orderModal.find('#delivery_address').empty().text(`${payload.street}, ${payload.city}, ${payload.state}, ${payload.zipcode}`);
    $orderModal.find('#contact_no').empty().text(`${payload.telephone}`);
    $orderModal.find('#order_summary tbody').empty();

    if (payload.type === 'Custom Order') {
        $orderModal.find('#table-headings').empty().append(
            `   <th scope="col" colspan="4">Services</th>
                <th scope="col">Total</th>`
        );

        renderQuoteItems(payload.desc, payload.get_total);
    } else {
        $orderModal.find('#table-headings').empty().append(
            `   <th scope="col">Service</th>
                <th scope="col">Quantity</th>
                <th scope="col">Unit Price</th>
                <th scope="col">Offers</th>
                <th scope="col">Total</th>`
        );

        payload.orderedservice_set.forEach(renderItems);
    }
    $orderModal.find('#order_summary tbody').append(`
                                                        <tr>
                                                            <td colspan="4" style="font-size: 15px"><strong>Total</strong>
                                                            </td>
                                                            <td style="font-size: 15px"><strong>${payload.get_total}</strong></td>
                                                        </tr>
    `);
    $orderModal.find('#order-reviews').empty().append(
        `<div class="row reviews alert alert-warning">
            <h6 class="pt-3 border-bottom"> Your review</h6>
            <div class="col-md col-lg">
                <p class="review-desc">
                    ${payload.review}
                </p>
                <!-- Star rating -->
                <span class="star-rating rev-rating"
                      data-rating="${payload.rating}">
                </span>
                <span class="review-date">${payload.rated_on} </span>
            </div>
        </div>`
    );

    starrateme();   // render rating stars

}


// create order status
function getOrderStatus(status) {
    ele = ''
    if (status === 'Processing') {
        ele = `Status: <i class="fa fa-cog fa-spin fa-fw"></i> ${status}`;
    } else if (status === 'Pending') {
        ele = `Status: <i class="fa fa-spinner fa-pulse fa-fw"></i> ${status}`;
    } else if (status === 'Delivered') {
        ele = `Status: <i class="fa fa-truck fa-fw"></i> ${status}`;
    } else {
        ele = `Status: <i class="fa fa-ban fa-stack-2x text-danger"></i> ${status}`;
    }
    return ele

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

// render order - quote
function renderQuoteItems(desc, get_total) {
    $orderModal.find('#order_summary tbody').append(
        `<tr>
                <td scope="col" colspan="4" id="p_name">
                    ${desc}
                </td>
                <td scope="col">${get_total}</td>
            </tr>`
    );
}

