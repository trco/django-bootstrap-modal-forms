/*
django-bootstrap-modal-forms
version : 1.5.0
Copyright (c) 2019 Uros Trstenjak
https://github.com/trco/django-bootstrap-modal-forms
*/

(function ($) {

    // Open modal & load the form at formURL to the modalContent element
    var newForm = function (modalID, modalContent, modalForm, formURL, errorClass, submitBtn) {
        $(modalID).find(modalContent).load(formURL, function () {
            $(modalID).modal("show");
            $(modalForm).attr("action", formURL);
            // Add click listener to the submitBtn
            addListeners(modalID, modalContent, modalForm, formURL, errorClass, submitBtn);
        });
    };

    // Submit form callback function
    var submitForm = function(modalForm) {
      $(modalForm).submit();
    };
    
    var addListeners = function (modalID, modalContent, modalForm, formURL, errorClass, submitBtn) {
        // submitBtn click listener
        $(submitBtn).on("click", function (event) {
            isFormValid(modalID, modalContent, modalForm, formURL, errorClass, submitBtn, submitForm);
        });
        // modal close listener
        $(modalID).on('hidden.bs.modal', function (event) {
            $(modalForm).remove();
        });
    };

    // Check if form.is_valid() & either show errors or submit it
    var isFormValid = function (modalID, modalContent, modalForm, formURL, errorClass, submitBtn, callback) {
        $.ajax({
            type: $(modalForm).attr("method"),
            url: $(modalForm).attr("action"),
            // Serialize form data
            data: $(modalForm).serialize(),
            beforeSend: function() {
                $(submitBtn).prop("disabled", true);
            },
            success: function (response) {
                if ($(response).find(errorClass).length > 0) {
                    // Form is not valid, update it with errors
                    $(modalID).find(modalContent).html(response);
                    $(modalForm).attr("action", formURL);
                    // Reinstantiate listeners
                    addListeners(modalID, modalContent, modalForm, formURL, errorClass, submitBtn);
                } else {
                    // Form is valid, submit it
                    callback(modalForm);
                }
            }
        });
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
