$(document).ready(function () {
    $('#style_form').on('submit', (function (event) {
        event.preventDefault();

        var data = {};
        data.heading = $('#heading_input').text();
        data.position = $('#number_position').val();
        data.style = $('#number_style').val();

        console.log(data);


        $.ajax({
            url: baseUrl + 'process/',
            data: JSON.stringify(data),
            type: 'POST',
            headers: {"X-CSRFToken": getCsrf()},
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                console.log('Processed');

            },
            error: function (data) {
                console.error('Difficulty parsing response')
            }
        });
    }));
});

