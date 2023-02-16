var $DOM = $(document);

$DOM.on('click', '#update_submit', function() {

	console.log("trip update clicked");
    data = {}
    data["departure"] = $(".departure").val();
    data["destination"] = $(".destination").val();
    data["vehicle_type"] = $(".vehicle_type").val();
    data["id"] = document.getElementById('trip-id').textContent;

    data["csrfmiddlewaretoken"] = window.CSRF_TOKEN

	$.ajax({
		type: 'post',
        data: JSON.stringify(data),
		url: '/trip/validate',
		success: function(result) {
            console.log(result);
            if (result.success) {
                window.location.href = "/my_ride"
            }
            else {
                alertify.set('notifier', 'position', 'top-right');
                alertify.error(result.message);
            }
		}
	});
});

$DOM.on('click', '#pickup_submit', function() {

	console.log("trip update clicked");
    data = {}
    data["pickup_time"] = new Date();
    data["id"] = document.getElementById('trip-id').textContent;

    data["csrfmiddlewaretoken"] = window.CSRF_TOKEN

	$.ajax({
		type: 'post',
        data: JSON.stringify(data),
		url: '/trip/pickup',
		success: function(result) {
            console.log(result);
            if (result.success) {
                window.location.href = "/my_ride"
            }
            else {
                alertify.set('notifier', 'position', 'top-right');
                alertify.error(result.message);
            }
		}
	});
});

$DOM.on('click', '#complete_submit', function() {

	console.log("trip update clicked");
    data = {}
    data["arrive_time"] = new Date();
    data["id"] = document.getElementById('trip-id').textContent;

    data["csrfmiddlewaretoken"] = window.CSRF_TOKEN

	$.ajax({
		type: 'post',
        data: JSON.stringify(data),
		url: '/trip/complete',
		success: function(result) {
            console.log(result);
            if (result.success) {
                window.location.href = "/my_ride"
            }
            else {
                alertify.set('notifier', 'position', 'top-right');
                alertify.error(result.message);
            }
		}
	});
});

$DOM.on('click', '#cancel_submit', function() {

	console.log("trip update clicked");
    data = {}
    data["id"] = document.getElementById('trip-id').textContent;

    data["csrfmiddlewaretoken"] = window.CSRF_TOKEN

	$.ajax({
		type: 'post',
        data: JSON.stringify(data),
		url: '/trip/cancel',
		success: function(result) {
            console.log(result);
            if (result.success) {
                window.location.href = "/my_ride"
            }
            else {
                alertify.set('notifier', 'position', 'top-right');
                alertify.error(result.message);
            }
		}
	});
});