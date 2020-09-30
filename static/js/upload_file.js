// Function to sumbit file to server and return document headings


// $(document).ready(function () {
//     $('#upload_form').on('submit', (function (event) {
//         event.preventDefault();
//         let data = new FormData(this);
//
//         //Passs form data to server
//         $.ajax({
//             url: baseUrl + 'upload/',
//             data: data,
//             type: 'POST',
//             contentType: false,
//             processData: false,
//             success: function (data) {
//
//                 $('#file_name').text(data['file_name']);
//
//
//                 // create a list of all the headings
//                 let heading_list = "<h3>Select a heading to start page numbering from</h3><ul class='scrollbar' id='headings' >"
//                 for (const [key, value] of Object.entries(data)) {
//                     if (key !== 'file_name') {
//                         heading_list += `<li id="heading_${value}" value="${value}">${key}</li>`
//                     }
//                 }
//                 heading_list += `</ul><button id='restart' onclick='restart()' title="Upload a new file">Start Again</button>`
//
//                 // Display the list on the webpage
//                 let h_list = $('#heading_list')
//                 h_list.html(heading_list);
//                 h_list.show();
//
//                 // Resize the content container so it can allow for two columns
//                 $(".content").css({"width": "968px", "justify-content": "space-between"});
//
//
//                 //display/hide instructions
//                 $('#welcome').hide();
//                 $('#style_form').show();
//
//
//                 // Function to allow list item to be selected
//                 $("#heading_list li").click(function () {
//                     let heading_input = $('#heading_input');
//                     heading_input.text($(this).val());
//                     heading_input.val($(this).text());
//
//                 });
//
//
//             },
//             error: function (data) {
//                 alert('Difficulty finding headers!\nPlease ensure that your file has headers set.');
//                 console.error('Difficulty parsing response')
//                 $("#file").val('');
//             }
//         });
//     }));
//
// })


//Function to test if file is correct format and not to big
$(document).ready(function () {
    $("#id_doc_file").change(function () {

        // Retrieve the filetype and assess if it is valid
        let file_type = this.files[0].name.split('.').pop();

        if (file_type !== 'docx') {
            alert("File format is incorrect!\n" +
                "Please select a .doc or .docx file.");
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

// Function to delete files and reload page
$(document).ready(function () {
    $('.restart').click(function (event) {
        event.preventDefault();

        let data = $("#pk").val();


        // Delete the file from the server if it exists
        if (data !== '') {
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
                    alert('Difficulty manually deleting files!\nAll files will automatically be deleted after 2 minutes.');
                    console.error('Difficulty deleting files')
                }
            });
        }

        //Reload the page
        location.reload();
    });
});

// Prevent the resubmission of form data when refreshing page
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}



