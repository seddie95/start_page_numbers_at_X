// Function to pass page specifications to server and return download link
$(document).ready(function () {
    $('#style_form').on('submit', (function (event) {
        event.preventDefault();

        let heading = $('#heading_input').text();

        if (heading !== '') {
            // Retrieve dictionary of form data
            let data = {};
            data.heading = heading;
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
                    // Set the download link to the returned sting and display it

                    // Resize the content container so it can allow for two columns
                    $(".content").css({"width": "720px", "justify-content": "space-between"});
                    $('#style_form').hide();
                    $('#heading_list').hide();
                    $("#download_link").attr("href", baseUrl + data);
                    $('#download_section').show();

                },
                error: function (data) {
                    console.error('Difficulty parsing response');

                }
            });
        } else {
            alert('Please Select a Heading');
        }

    }));
});

