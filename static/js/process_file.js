// Function to pass page specifications to server and return download link
$(document).ready(function () {
    $('#style_form').on('submit', (function (event) {
        event.preventDefault();

        // Retrieve dictionary of form data
        let data = {};
        data.heading = $('#heading_input').text();
        data.position = $('#number_position').val();
        data.style = $('#number_style').val();
        data.file_name = $('#file_name').text();

        // Send form data to server
        $.ajax({
            url: baseUrl + 'process/',
            data: JSON.stringify(data),
            type: 'POST',
            headers: {"X-CSRFToken": getCsrf()},
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                // Set the download link to the returned sting
                let download_link = $("#download_link")
                download_link.attr("href", baseUrl + data);
                download_link.show();
                $('#bullets').hide();
                $('#item_3').show();
            },
            error: function (data) {
                console.error('Difficulty parsing response');

            }
        });
    }));
});

