//Function to test if file is correct format and not to big
$(document).ready(function () {
    $("#id_doc_file").change(function () {

        // Retrieve the filetype and assess if it is valid
        let file_type = this.files[0].name.split('.').pop();

        if (file_type !== 'docx') {
            alert("File format is incorrect!\n" +
                "Please upload a .docx file.");
            this.value = "";
        }
        // Prevent large file upload
        else if (this.files[0].size > 20000000) {
            alert("File is too big!");
            this.value = "";
        } else {
            //trigger the upload
            $('#upload_form').trigger('submit');
        }

    })
})
//=============================================================================

// Function to delete files and reload page
$(document).ready(function () {
    $('.restart').click(function (event) {
        event.preventDefault();

        // Retrieve the primary key
        let data = $("#pk").val();

        // Delete the file from the server if it exists
        if (data) {
            // Pass file_name to server
            $.ajax({
                url: baseUrl + 'delete/',
                data: JSON.stringify(data),
                type: 'POST',
                headers: {"X-CSRFToken": getCsrf()},
                dataType: 'json',
                contentType: 'application/json',
                success: function (data) {
                    console.log(data);
                },
                error: function (data) {
                    alert('Difficulty manually deleting files!' +
                        '\nAll files will automatically be deleted after 2 minutes.');
                    console.error('Difficulty deleting files')
                }
            });
            //Reload the page
            location.reload();

        } else {
            // Go to the homepage
            location.href = '/';
        }

    });
});

//=============================================================================

// Function to allow list item to be selected
$(document).ready(function () {
    $("#heading_list li").click(function () {
        let heading_input = $('#heading_input');
        heading_input.text($(this).text());
        heading_input.val($(this).val());
    });
});

//=============================================================================

// Prevent the resubmission of form data when refreshing page
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}
// Return user to homepage if back button is pressed
if (performance.navigation.type === 2) {
    location.href = '/';
}

// Return user to homepage if refresh button is pressed
if (performance.navigation.type === 1) {
    location.href = '/';
}

//=============================================================================
//function to inform that file will be deleted after 2 minutes
$(window).on('load', function () {
    if (document.URL.includes("process") || document.URL.includes("download")) {
        setTimeout(function (event) {
            location.href = '/reupload'

        }, 120000);
    }
})


//=============================================================================
// Function to only submit headings by clicking on list of headings
$(document).ready(function () {
    $(".readonly").on('keydown paste', function (e) {
        e.preventDefault();
    });
});

