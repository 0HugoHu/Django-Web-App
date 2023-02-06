var $DOM = $(document);

$DOM.on('click', '#signup_submit', function() {

	console.log("submit clicked");
    data = {}
    data["first_name"] = $(".first_name").val();
    data["last_name"] = $(".last_name").val();
    data["username"] = $(".username").val();
    data["gender"] = $(".gender").val();
    data["password"] = $(".password").val();
    data["confirm_password"] = $(".confirm_password").val();
    data["phone_number"] = $(".phone_number").val();
    data["is_driver"] = document.querySelector('#user_type').checked;
    data["driver_license"] = $(".driver_license").val();
    data["plate_number"] = $(".plate_number").val();
    data["email"] = $(".email").val();

	$.ajax({
		type: 'post',
        data: JSON.stringify(data),
		url: '/signup/validate',
		success: function(result) {
            console.log(result);
            if (result.success) {
                window.location.href = "/login"
            }
            else {
                alertify.set('notifier', 'position', 'top-right');
                alertify.error(result.message);
            }
		}
	});
});

