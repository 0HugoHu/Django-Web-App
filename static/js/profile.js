var $DOM = $(document);

$DOM.on('click', '#update_submit', function() {

	console.log("profile update clicked");
    data = {}
    data["username"] = $(".username").val();
    data["gender"] = $(".gender").val();
    data["password"] = $(".password").val();
    data["phone_number"] = $(".phone_number").val();
    data["is_driver"] = document.querySelector('#user_type').checked;
    data["driver_license"] = $(".driver_license").val();
    data["plate_number"] = $(".plate_number").val();
    data["email"] = document.getElementById('email').placeholder;

	$.ajax({
		type: 'post',
        data: JSON.stringify(data),
		url: '/profile/validate',
		success: function(result) {
            console.log(result);
            if (result.success) {
                window.location.href = "/profile"
            }
            else {
                alertify.set('notifier', 'position', 'top-right');
                alertify.error(result.message);
            }
		}
	});
});

