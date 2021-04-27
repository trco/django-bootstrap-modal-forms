/*
django-bootstrap-modal-forms
version : 2.2.0
Copyright (c) 2021 Uros Trstenjak
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
        $(settings.modalForm).on("submit", function (event) {
            if (event.originalEvent !== undefined && settings.isDeleteForm === false) {
                event.preventDefault();
                isFormValid(settings, submitForm);
                return false;
            }
        });
        // Modal close handler
        $(settings.modalID).on("hidden.bs.modal", function (event) {
            $(settings.modalForm).remove();
        });
    };

    // Check if form.is_valid() & either show errors or submit it via callback
    var isFormValid = function (settings, callback) {
        $.ajax({
            type: $(settings.modalForm).attr("method"),
            url: $(settings.modalForm).attr("action"),
            data: new FormData($(settings.modalForm)[0]),
            contentType: false,
            processData: false,
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

    // Submit form callback function
    var submitForm = function (settings) {        
        if (!settings.asyncUpdate) {
            $(settings.modalForm).submit();
        } else {          
            var asyncSettingsValid = validateAsyncSettings(settings.asyncSettings);
            
            if (asyncSettingsValid) {                
                var asyncSettings = settings.asyncSettings;
                // Serialize form data
                var formdata = new FormData($(settings.modalForm)[0]);
                // Add asyncUpdate and check for it in save method of CreateUpdateAjaxMixin
                formdata.append("asyncUpdate", "True");
                
                $.ajax({
                    type: $(settings.modalForm).attr("method"),
                    url: $(settings.modalForm).attr("action"),
                    data: formdata,
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        var body = $("body");
                        if (body.length === 0) {
                            console.error("django-bootstrap-modal-forms: <body> element missing in your html.");
                        }
                        body.prepend(asyncSettings.successMessage);
    
                        // Update page without refresh
                        $.ajax({
                            type: "GET",
                            url: asyncSettings.dataUrl,
                            dataType: "json",
                            success: function (response) {
                                // Update page
                                $(asyncSettings.dataElementId).html(response[asyncSettings.dataKey]);
    
                                // Add modalForm to trigger element after async page update
                                if (asyncSettings.addModalFormFunction) {
                                    asyncSettings.addModalFormFunction();
                                }
    
                                if (asyncSettings.closeOnSubmit) {
                                    $(settings.modalID).modal("hide");
                                } else {
                                    // Reload form
                                    $(settings.modalID).find(settings.modalContent).load(settings.formURL, function () {
                                        $(settings.modalForm).attr("action", settings.formURL);
                                        addEventHandlers(settings);
                                    });
                                }
                            }
                        });
                    }
                });
            }
        }
    };

    var validateAsyncSettings = function (settings) {
        var missingSettings = [];

        if (!settings.successMessage) {
            missingSettings.push("successMessage");
            console.error("django-bootstrap-modal-forms: 'successMessage' in asyncSettings is missing.");
        }        
        if (!settings.dataUrl) {
            missingSettings.push("dataUrl");
            console.error("django-bootstrap-modal-forms: 'dataUrl' in asyncSettings is missing.");
        }
        if (!settings.dataElementId) {
            missingSettings.push("dataElementId");
            console.error("django-bootstrap-modal-forms: 'dataElementId' in asyncSettings is missing.");
        }
        if (!settings.dataKey) {
            missingSettings.push("dataKey");
            console.error("django-bootstrap-modal-forms: 'dataKey' in asyncSettings is missing.");
        }
        if (!settings.addModalFormFunction) {
            missingSettings.push("addModalFormFunction");
            console.error("django-bootstrap-modal-forms: 'addModalFormFunction' in asyncSettings is missing.");
        }

        if (missingSettings.length > 0) {
            return false;
        }

        return true;
    };

    $.fn.modalForm = function (options) {
        // Default settings
        var defaults = {
            modalID: "#modal",
            modalContent: ".modal-content",
            modalForm: ".modal-content form",
            formURL: null,
            isDeleteForm: false,
            errorClass: ".invalid",
            asyncUpdate: false,
            asyncSettings: {
                closeOnSubmit: false,
                successMessage: null,
                dataUrl: null,
                dataElementId: null,
                dataKey: null,
                addModalFormFunction: null
            }
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
