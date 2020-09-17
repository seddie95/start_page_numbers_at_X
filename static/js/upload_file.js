$(document).ready(function () {
    $('#upload_form').on('submit', (function (event) {
        event.preventDefault();
        var data = new FormData(this);


        $.ajax({
            url: baseUrl + 'upload/',
            data: data,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function (data) {
                let heading_list = "<ul>"
                for (const [key, value] of Object.entries(data)) {
                    heading_list += `<li id="heading_${value}" value="${value}">${key}</li>`
                }
                heading_list += "</ul>"

                $('#heading_list').html(heading_list);

                $("#heading_list li").click(function () {
                    let heading_input = $('#heading_input');
                    heading_input.text($(this).val());
                    heading_input.val($(this).text());
                });

            },
            error: function (data) {
                console.error('Difficulty parsing response')
            }
        });
    }));
});

