
$(document).ready(function () {

	var myApp = new Vue({
		el: '#myVueAppContainer',
		type: 'POST',
		data: {
            flapping_services: [],
            currently_down: [],
            recently_down: []
		}
	});

	$('#analyzeButtonOne').on('click', function () {
        $.ajax({
            url: 'input_json.json',
            type: 'GET',
            dataType: 'json'
        }).then(function(data){
            $.ajax({
                url: 'http://localhost:8000/analyze_json_type_one',
                type: 'POST',
                data: JSON.stringify (data),
                dataType: 'json',
                success:function(data) {
                    myApp.flapping_services = data.flapping_services;
                    myApp.currently_down = data.currently_down;
                    myApp.recently_down = data.recently_down;
                },
                contentType: 'application/json'
            });
        });
	});

	$('#analyzeButtonTwo').on('click', function () {
        $.ajax({
            url: 'input_json.json',
            type: 'GET',
            dataType: 'json'
        }).then(function(data){
            $.ajax({
                url: 'http://localhost:8000/analyze_json_type_two',
                type: 'POST',
                data: JSON.stringify (data),
                dataType: 'json',
                success:function(data) {
                    myApp.flapping_services = data.flapping_services;
                    myApp.currently_down = data.currently_down;
                    myApp.recently_down = data.recently_down;
                },
                contentType: 'application/json'
            });
        });
	});
});


