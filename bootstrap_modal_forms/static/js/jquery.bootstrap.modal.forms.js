/*
django-bootstrap-modal-forms
version : 2.0.0
Copyright (c) 2020 Uros Trstenjak
https://github.com/trco/django-bootstrap-modal-forms
*/

(function ($) {

    // Open modal & load the form at formURL to the modalContent element
    var modalForm = function (settings) {
        $(settings.modalID).find(settings.modalContent).load(settings.formURL, function () {
            $(settings.modalID).modal("show");
            $(settings.modalForm).attr("action", settings.formURL);
            addEventHandlers(settings);
        });
    };

    var addEventHandlers = function (settings) {
        // submitBtn click handler
        $(settings.submitBtn).on("click", function (event) {
            isFormValid(settings, submitForm);
        });
        // Modal close handler
        $(settings.modalID).on("hidden.bs.modal", function (event) {
            $(settings.modalForm).remove();
        });
    };

    // Submit form callback function
    var submitForm = function (settings) {
        if (settings.closeOnSubmit) {
            $(settings.modalForm).submit();
        } else {
            $.ajax({
                type: $(settings.modalForm).attr("method"),
                url: $(settings.modalForm).attr("action"),
                // Add closeOnSubmit and check for it in save method of CreateUpdateAjaxMixin
                data: $(settings.modalForm).serialize() + "&closeOnSubmit=False",
                success: function (response) {
                    $(settings.modalID).prepend(settings.ajaxSuccessMessage);

                    // Update page without refresh
                    $.ajax({
                        type: "GET",
                        url: settings.dataUrl,
                        dataType: "json",
                        success: function (response) {
                            // Reload form
                            $(settings.modalID).find(settings.modalContent).load(settings.formURL, function () {
                                $(settings.modalForm).attr("action", settings.formURL);
                                addEventHandlers(settings);
                            });

                            // Update page
                            $(settings.dataElementId).html(response[settings.dataKey]);
                            
                            // Add modalForm to trigger element after ajax page update
                            if (settings.addModalFormFunction) {
                                settings.addModalFormFunction();
                            }
                        }
                    });
                }
            });
        }
    };

    // Check if form.is_valid() & either show errors or submit it via callback
    var isFormValid = function (settings, callback) {
        $.ajax({
            type: $(settings.modalForm).attr("method"),
            url: $(settings.modalForm).attr("action"),
            data: $(settings.modalForm).serialize(),
            beforeSend: function () {
                $(settings.submitBtn).prop("disabled", true);
            },
            success: function (response) {
                if ($(response).find(settings.errorClass).length > 0) {
                    // Form is not valid, update it with errors
                    $(settings.modalID).find(settings.modalContent).html(response);
                    $(settings.modalForm).attr("action", settings.formURL);
                    // Reinstantiate handlers
                    addEventHandlers(settings);
                } else {
                    // Form is valid, submit it
                    callback(settings);
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
            submitBtn: ".submit-btn",
            closeOnSubmit: true,
            ajaxSuccessMessage: null,
            dataUrl: null,
            dataElementId: null,
            dataKey: null,
            addModalFormFunction: null
        };

        // Extend default settings with provided options
        var settings = $.extend(defaults, options);

        this.each(function () {
            // Add click event handler to the element with attached modalForm
            $(this).click(function (event) {
                // Instantiate new form in modal
                modalForm(settings);
            });
        });

        return this;
    };

}(jQuery));