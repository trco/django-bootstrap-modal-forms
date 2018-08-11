/*
django-bootstrap-modal-forms
version : 1.1.0
Copyright (c) 2018 Uros Trstenjak
https://github.com/trco/django-bootstrap-modal-forms
*/

(function ($) {

    // Place the form at formURL to modalContent element of modal with id=modalID
    var newForm = function (modalID, modalContent, modalForm, formURL, successURL, errorClass) {
        $(modalContent).load(formURL, function () {
            $(modalID).modal('toggle');
            ajaxSubmit(modalID, modalContent, modalForm, successURL, errorClass);
        });
    };

    // Add AJAX validation to the modalForm
    var ajaxSubmit = function (modalID, modalContent, modalForm, successURL, errorClass) {
        $(modalForm).submit(function (event) {
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
                        $(modalID).find(modalContent).html(response);
                        ajaxSubmit(modalID, modalContent, modalForm, successURL, errorClass);
                    }
                    // Hide modal after successful POST request when & redirect to successURL
                    else {
                        $(modalID).modal("hide");
                        window.location.href = successURL;
                    }
                }
            });
        });
    };

    $.fn.modalForm = function (options) {
        // Default settings
        var defaults = {
            modalID: "#modal",
            modalContent: ".modal-content",
            modalForm: ".modal-content form",
            formURL: null,
            successURL: "/",
            errorClass: ".invalid"
        };

        // Extend default settings with provided options
        var settings = $.extend(defaults, options);

        return this.each(function () {
            $(this).click(function (event) {
                newForm(settings.modalID,
                    settings.modalContent,
                    settings.modalForm,
                    settings.formURL,
                    settings.successURL,
                    settings.errorClass);
                event.preventDefault();
            });
        });
    };

}(jQuery));