// profile pic upload btn
$(".profile-pic-edit").click(function () {
    $("input[type='file']").trigger('click');


  });
// preview
id_profile_pic.onchange = function (event) {
    frame.src=URL.createObjectURL(event.target.files[0]);
}

// when edit button clicked
$("#editProfile").click(function(){
    $(this).addClass('d-none');
    $('#saveProfile').removeClass('d-none');
    $('#personalDetails').find('input').removeAttr('readonly');
});