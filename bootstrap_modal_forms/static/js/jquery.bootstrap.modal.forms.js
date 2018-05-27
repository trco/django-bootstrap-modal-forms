/*
django-bootstrap-modal-forms
version : 1.0
Copyright (c) 2018 Uros Trstenjak
https://github.com/trco/django-bootstrap-modal-forms
*/

(function ($) {

    // Place the form at formURL to modalContent element of modal with id=modalID
    var newForm = function (modalContent, formURL, modalID, modalForm, errorClass) {
        $(modalContent).load(formURL, function () {
            $(modalID).modal('toggle');
            ajaxSubmit(modalForm, modalID, modalContent, errorClass);
        });
    };

    // Add AJAX validation to the modalForm
    var ajaxSubmit = function (form, modal, modalContent, errorClass) {
        $(form).submit(function (event) {
            // Prevent submit and POST form to url using AJAX
            event.preventDefault();
            $.ajax({
                type: $(this).attr("method"),
                url: $(this).attr("action"),
                // Serialize form data
                data: $(this).serialize(),
                success: function (response) {
                    // Update form with errors after unsuccessful POST request
                    // Django form.is_valid() = False
                    if ($(response).find(errorClass).length > 0) {
                        $(modal).find(modalContent).html(response);
                        ajaxSubmit(form, modal, modalContent, errorClass);
                    }
                    // Hide modal after successful POST request
                    // Django form.is_valid() = True
                    else {
                        $(modal).modal("hide");
                    }
                }
            });
        });
    };

    $.fn.modalForm = function (options) {
        // Default settings
        var defaults = {
            modalContent: ".modal-content",
            formURL: null,
            modalID: "#modal",
            modalForm: ".modal-content form",
            errorClass: ".invalid"
        };

        // Extend default settings with provided options
        var settings = $.extend(defaults, options);

        return this.each(function () {
            $(this).click(function (event) {
                newForm(settings.modalContent,
                    settings.formURL,
                    settings.modalID,
                    settings.modalForm,
                    settings.errorClass);
                event.preventDefault();
            });
        });
    };

}(jQuery));