$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
    $('[data-toggle="tooltip"]').on('shown.bs.tooltip', function () {
        $('.tooltip').addClass('animated tada');
    })
});

function validateFault() {
    let validation = true;

    let phone_number = document.getElementById("phone_number");
    let object_number = document.getElementById("object_number").value;
    let topic = document.getElementById("topic").value;
    let description = document.getElementById("description").value;

    let phone_number_alert = document.getElementById("phone_number_alert");
    let object_number_alert = document.getElementById("object_number_alert");
    let topic_alert = document.getElementById("topic_alert");
    let description_alert = document.getElementById("description_alert");

    let object_number_regex = new RegExp("^([0-9]{10})$");
    let phone_number_regex = new RegExp("^([+]?[1]?[0-9]{9,15})$");

    if (phone_number) {
        if (!phone_number.value) {
            validation = false;
            $('#phone_number').attr('data-original-title', 'phone number is required')
                .tooltip('fixTitle')
                .tooltip('show');
        }
        else {
            if (!phone_number_regex.test(phone_number.value)) {
                validation = false;
                $('#phone_number').attr('data-original-title', 'allowed phone number format: +999999999 (9-15 digits with possible plus)')
                    .tooltip('fixTitle')
                    .tooltip('show');
            }
            else {
                $('#phone_number').tooltip('hide');
            }
        }
    }

    if (!object_number) {
        validation = false;
        $('#object_number').attr('data-original-title', 'object number is required')
                           .tooltip('fixTitle')
                           .tooltip('show');
    }
    else {
        if (!object_number_regex.test(object_number)) {
            validation = false;
            $('#object_number').attr('data-original-title', 'allowed object number format: 9999999999 (10 digits)')
                               .tooltip('fixTitle')
                               .tooltip('show');
        }
        else {
            $('#object_number').tooltip('hide');
        }
    }

    if (!topic) {
        validation = false;
        $('#topic').attr('data-original-title', 'topic is required')
                   .tooltip('fixTitle')
                   .tooltip('show');
    }
    else {
        if (topic.length > 50) {
            validation = false;
            $('#topic').attr('data-original-title', 'allowed topic max length: 50 signs')
                       .tooltip('fixTitle')
                       .tooltip('show');
        }
        else {
            $('#topic').tooltip('hide');
        }
    }

    if (!description) {
        validation = false;
        $('#description').attr('data-original-title', 'description is required')
                         .tooltip('fixTitle')
                         .tooltip('show');
    }
    else {
        if (description.length > 200) {
            validation = false;
            $('#description').attr('data-original-title', 'allowed description max length: 200 signs')
                             .tooltip('fixTitle')
                             .tooltip('show');
        }
        else {
            $('#description').tooltip('hide');
        }
    }

    if (validation) {
        $.confirm({
            title: 'confirm!',
            content: 'are you sure you want to do this??',
            type: 'red',
            buttons: {
                confirm: function () {
                    $('#fault-form').submit();
                },
                cancel: function () {
                }
            }
        });
    }
}