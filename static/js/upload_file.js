// Function to sumbit file to server and return document headings
$(document).ready(function () {
    $('#upload_form').on('submit', (function (event) {
        event.preventDefault();
        var data = new FormData(this);

        //Passs form data to server
        $.ajax({
            url: baseUrl + 'upload/',
            data: data,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function (data) {

                $('#file_name').text(data['file_name'])

                // create a list of all the headings
                let heading_list = "<ul>"
                for (const [key, value] of Object.entries(data)) {
                    if (key !== 'file_name') {
                        heading_list += `<li id="heading_${value}" value="${value}">${key}</li>`
                    }
                }
                heading_list += "</ul>"

                // Display the list on the webpage
                $('#heading_list').html(heading_list);

                // Function to allow list item to be selected
                $("#heading_list li").click(function () {
                    let heading_input = $('#heading_input');
                    heading_input.text($(this).val());
                    heading_input.val($(this).text());
                });

            },
            error: function (data) {
                alert('Difficulty finding headers!\nPlease ensure that your file has headers set.');
                console.error('Difficulty parsing response')
                $("#file").val('');
            }
        });
    }));

})


//Function to test if file is correct format and not to big
$(document).ready(function () {
    $("#file").change(function () {

        // Retrieve the filetype and assess if it is valid
        let file_type = this.files[0].name.split('.').pop();

        if (file_type !== 'docx') {
            alert("File format is incorrect!\n" +
                "Please select a .doc or .docx file.");
            this.value = "";
        }
        // Prevent large file upload
        else if (this.files[0].size > 200000000) {
            alert("File is too big!");
            this.value = "";
        } else {
            //trigger the upload
            $('#upload_form').trigger('submit');
        }

    })
})