var $DOM = $(document);

$DOM.on('click', '#update_submit', function() {

	console.log("profile update clicked");
    data = {}
    data["brand"] = $(".brand").val();
    data["model"] = $(".model").val();
    data["vehicle_type"] = $(".vehicle_type").val();
    data["capacity"] = $(".capacity").val();
    data["year"] = $(".year").val();
    data["color"] = $(".color").val();
    data["plate_number"] = document.getElementById('plate-number').textContent;
    console.log(data["plate_number"]);
	$.ajax({
		type: 'post',
        data: JSON.stringify(data),
		url: '/vehicle/validate',
		success: function(result) {
            console.log(result);
            if (result.success) {
                window.location.href = "/"
            }
            else {
                alertify.set('notifier', 'position', 'top-right');
                alertify.error(result.message);
            }
		}
	});
});