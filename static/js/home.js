var $DOM = $(document);
$DOM.on('click', '#search_submit', function() {
	departure = $(".departure").val();
	destination = $(".destination").val();
	if(departure === "" || destination === "") {
		console.log("empty search")
	} else {
		const prefix_time = "Estimate arrives at: ";
		const collection = document.getElementsByClassName("estimate_time");
		const collection2 = document.getElementsByClassName("estimate_price");
		const base_Price = Math.floor(Math.random() * 35) + 10;
		time = parseInt($(".leave-time-time").val());
		for (let i = 0; i < 6; i++) {
			const d = new Date();
			d.setMinutes(d.getMinutes() + Math.floor(Math.random() * 30) + time);
			collection[i].textContent = prefix_time + ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2);
			let randomNum = Math.random() * 10 + 5;
			if (i === 4) {
				collection2[4].textContent = "" + ((base_Price + 1.2 * randomNum).toFixed(2));
			} else {
				collection2[i].textContent = "" + ((base_Price + (i + 1) * randomNum).toFixed(2));
			}
			}
		$('.search_results').empty()
		console.log("search clicked");
	}
});

$DOM.on('click', '#choice_1', function() {
    departure = $(".departure").val();
	destination = $(".destination").val();
	joinShared = document.querySelector('#is_shared').checked;
	const collection = document.getElementsByClassName("estimate_time");
	const collection2 = document.getElementsByClassName("estimate_price");
	estimatePickUpTime = collection[0].textContent.split(' ')[3];
	estimateFee = collection2[0].textContent;
	email = document.getElementsByClassName("user-email")[0].textContent;

	console.log("trip requested");
	$.ajax({
		type: 'get',
		url: '/search?email=' + email + '&departure=' + departure + '&destination=' + destination + '&joinShared=' + joinShared + '&estimatePickUpTime=' + estimatePickUpTime + '&estimateFee=' + estimateFee + '&choice=' + 1,
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

$DOM.on('click', '#choice_2', function() {
    departure = $(".departure").val();
	destination = $(".destination").val();
	joinShared = document.querySelector('#is_shared').checked;
	const collection = document.getElementsByClassName("estimate_time");
	const collection2 = document.getElementsByClassName("estimate_price");
	estimatePickUpTime = collection[1].textContent.split(' ')[3];
	estimateFee = collection2[1].textContent;
	email = document.getElementsByClassName("user-email")[0].textContent;

	console.log("trip requested");
	$.ajax({
		type: 'get',
		url: '/search?email=' + email + '&departure=' + departure + '&destination=' + destination + '&joinShared=' + joinShared + '&estimatePickUpTime=' + estimatePickUpTime + '&estimateFee=' + estimateFee + '&choice=' + 2,
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

$DOM.on('click', '#choice_3', function() {
    departure = $(".departure").val();
	destination = $(".destination").val();
	joinShared = document.querySelector('#is_shared').checked;
	const collection = document.getElementsByClassName("estimate_time");
	const collection2 = document.getElementsByClassName("estimate_price");
	estimatePickUpTime = collection[2].textContent.split(' ')[3];
	estimateFee = collection2[2].textContent;
	email = document.getElementsByClassName("user-email")[0].textContent;

	console.log("trip requested");
	$.ajax({
		type: 'get',
		url: '/search?email=' + email + '&departure=' + departure + '&destination=' + destination + '&joinShared=' + joinShared + '&estimatePickUpTime=' + estimatePickUpTime + '&estimateFee=' + estimateFee + '&choice=' + 3,
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

$DOM.on('click', '#choice_4', function() {
    departure = $(".departure").val();
	destination = $(".destination").val();
	joinShared = document.querySelector('#is_shared').checked;
	const collection = document.getElementsByClassName("estimate_time");
	const collection2 = document.getElementsByClassName("estimate_price");
	estimatePickUpTime = collection[3].textContent.split(' ')[3];
	estimateFee = collection2[3].textContent;
	email = document.getElementsByClassName("user-email")[0].textContent;

	console.log("trip requested");
	$.ajax({
		type: 'get',
		url: '/search?email=' + email + '&departure=' + departure + '&destination=' + destination + '&joinShared=' + joinShared + '&estimatePickUpTime=' + estimatePickUpTime + '&estimateFee=' + estimateFee + '&choice=' + 4,
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

$DOM.on('click', '#choice_5', function() {
    departure = $(".departure").val();
	destination = $(".destination").val();
	joinShared = document.querySelector('#is_shared').checked;
	const collection = document.getElementsByClassName("estimate_time");
	const collection2 = document.getElementsByClassName("estimate_price");
	estimatePickUpTime = collection[4].textContent.split(' ')[3];
	estimateFee = collection2[4].textContent;
	email = document.getElementsByClassName("user-email")[0].textContent;

	console.log("trip requested");
	$.ajax({
		type: 'get',
		url: '/search?email=' + email + '&departure=' + departure + '&destination=' + destination + '&joinShared=' + joinShared + '&estimatePickUpTime=' + estimatePickUpTime + '&estimateFee=' + estimateFee + '&choice=' + 5,
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

$DOM.on('click', '#choice_6', function() {
    departure = $(".departure").val();
	destination = $(".destination").val();
	joinShared = document.querySelector('#is_shared').checked;
	const collection = document.getElementsByClassName("estimate_time");
	const collection2 = document.getElementsByClassName("estimate_price");
	estimatePickUpTime = collection[5].textContent.split(' ')[3];
	estimateFee = collection2[5].textContent;
	email = document.getElementsByClassName("user-email")[0].textContent;

	console.log("trip requested");
	$.ajax({
		type: 'get',
		url: '/search?email=' + email + '&departure=' + departure + '&destination=' + destination + '&joinShared=' + joinShared + '&estimatePickUpTime=' + estimatePickUpTime + '&estimateFee=' + estimateFee + '&choice=' + 6,
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
