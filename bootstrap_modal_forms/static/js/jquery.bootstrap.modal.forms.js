/*
django-bootstrap-modal-forms
version : 1.3.1
Copyright (c) 2018 Uros Trstenjak
https://github.com/trco/django-bootstrap-modal-forms
*/

(function ($) {

    // Open modal & load the form at formURL to the modalContent element
    var newForm = function (modalID, modalContent, modalForm, formURL, errorClass, submitBtn) {
        $(modalContent).load(formURL, function () {
            $(modalID).modal("show");
            $(modalForm).attr("action", formURL);
            // Add click listener to the submitBtn
            ajaxSubmit(modalID, modalContent, modalForm, formURL, errorClass, submitBtn);
        });
    };

    // Add click listener to the submitBtn
    var ajaxSubmit = function (modalID, modalContent, modalForm, formURL, errorClass, submitBtn) {
        $(submitBtn).on("click", function () {
            // Check if form.is_valid() via ajax request
            var formIsValid = isFormValid(modalID, modalContent, modalForm, formURL, errorClass);
            if (formIsValid) {
                // Submit form if form.is_valid()
                $(modalForm).submit();
            } else {
                // Reinstantiate click listener on submitBtn
                // Form is updated with errors in isFormValid(...) call
                ajaxSubmit(modalID, modalContent, modalForm, formURL, errorClass, submitBtn);
            }
        });
    };

    // Check if form.is_valid()
    var isFormValid = function (modalID, modalContent, modalForm, formURL, errorClass) {
        var formIsValid = true;
        $.ajax({
            type: $(modalForm).attr("method"),
            url: $(modalForm).attr("action"),
            async: false,
            // Serialize form data
            data: $(modalForm).serialize(),
            success: function (response) {
                if ($(response).find(errorClass).length > 0) {
                    formIsValid = false;
                    // Update form with errors if not form.is_valid()
                    $(modalID).find(modalContent).html(response);
                    $(modalForm).attr("action", formURL);
                }
            }
        });
        return formIsValid;
    };

    $.fn.modalForm = function (options) {
        // Default settings
        var defaults = {
            modalID: "#modal",
            modalContent: ".modal-content",
            modalForm: ".modal-content form",
            formURL: null,
            errorClass: ".invalid",
            submitBtn: ".submit-btn"
        };

        // Extend default settings with provided options
        var settings = $.extend(defaults, options);

        return this.each(function () {
            // Add click listener to the element with attached modalForm
            $(this).click(function (event) {
                // Instantiate new modalForm in modal
                newForm(settings.modalID,
                    settings.modalContent,
                    settings.modalForm,
                    settings.formURL,
                    settings.errorClass,
                    settings.submitBtn);
            });
        });
    };

}(jQuery));