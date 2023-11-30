'use strict';
/*
django-bootstrap-modal-forms
version : 2.2.1
Copyright (c) 2023 Marcel Rupp
*/

/**
 * Open modal & load the form as inner HTML from "formURL" to the "modalContent" element
 *
 * @param {Object} settings Configuration/Settings for associated modal
 */
const modalFormCallback = function (settings) {
    let modal = document.querySelector(settings.modalID);
    let content = modal.querySelector(settings.modalContent);

    let modalInstance = bootstrap.Modal.getInstance(modal);
    if (modalInstance === null) {
        modalInstance = new bootstrap.Modal(modal, {
            keyboard: false
        })
    }

    fetch(settings.formURL, {credentials: settings.credentials}).then(res => {
        // Get content from target URL
        return res.text();
    }).then(data => {
        // Set content to inner HTML
        content.innerHTML = data;
    }).then(() => {
        // Finally show the modal with new content
        modalInstance.show();

        let form = modal.querySelector(settings.modalForm);
        if (form) {
            form.action = settings.formURL;
            // Add handler for form validation
            addEventHandlers(modal, form, settings);
        }
    });
};

/**
 * Adds event handler for form validation cycle.
 *
 * @param {HTMLElement} modal The modal
 * @param {HTMLElement} form The actual form, that should be evaluated by the server
 * @param {Object} settings Configuration/Settings for associated modal
 */
const addEventHandlers = function (modal, form, settings) {
    form.addEventListener('submit', (event) => {
        if (settings.isDeleteForm === false) {
            event.preventDefault();
            isFormValid(settings, submitForm);
            return false;
        }
    });

    modal.addEventListener('hidden.bs.modal', () => {
        let content = modal.querySelector(settings.modalContent);
        while (content.lastChild) {
            content.removeChild(content.lastChild);
        }
    });
};

/**
 * Sends the form to the server & processes the result. If the form is valid the redirect from the
 * form will be executed. If the form is invalid the errors are shown and no redirect will be executed.
 *
 * @param {Object} settings Configuration/Settings for associated modal
 * @param {Function} callback Callback to break out of form validation cycle
 */
const isFormValid = function (settings, callback) {
    let modal = document.querySelector(settings.modalID);
    let form = modal.querySelector(settings.modalForm);
    let headers = new Headers();
    headers.append('X-Requested-With', 'XMLHttpRequest');

    let btnSubmit = modal.querySelector('button[type="submit"]');
    btnSubmit.disabled = true;

    fetch(form.action, {
        headers: headers,
        method: form.method,
        body: new FormData(form),
        credentials: settings.credentials,
    }).then(res => {
        return res.text();
    }).then(data => {
        // console.log(data)
        if (data.includes(settings.errorClass)) {
            // Form is invalid, therefore set the returned form (with marked invalid fields) to new inner HTML
            modal.querySelector(settings.modalContent).innerHTML = data;

            form = modal.querySelector(settings.modalForm);
            if (!form) {
                console.error('no form present in response')
                return;
            }

            // Start from the beginning
            form.action = settings.formURL;
            addEventHandlers(modal, form, settings)
        } else {
            callback(settings);
        }
    });
};

/**
 * Submit form callback function
 *
 * @param {Object} settings Configuration/Settings for associated modal
 */
const submitForm = function (settings) {
    let modal = document.querySelector(settings.modalID);
    let form = modal.querySelector(settings.modalForm);

    if (!settings.asyncUpdate) {
        form.submit();
    } else {
        const asyncSettingsValid = validateAsyncSettings(settings.asyncSettings);
        if (asyncSettingsValid) {
            let asyncSettings = settings.asyncSettings;
            // Serialize form data
            let formData = new FormData(form);
            // Add asyncUpdate and check for it in save method of CreateUpdateAjaxMixin
            formData.append("asyncUpdate", "True");

            fetch(form.action, {
                method: form.method,
                body: formData,
                credentials: settings.credentials,
            }).then(res => {
                return res.text();
            }).then(data => {
                let body = document.body;
                if (body === undefined) {
                    console.error("django-bootstrap-modal-forms: <body> element missing in your html.");
                    return;
                }

                let doc = new DOMParser().parseFromString(asyncSettings.successMessage, "text/xml");
                body.insertBefore(doc.firstChild, body.firstChild);

                if (asyncSettings.dataUrl) {
                    // Update page without refresh
                    fetch(asyncSettings.dataUrl, {credentials: settings.credentials}).then(res => res.json()).then(data => {
                        // Update page
                        let dataElement = document.querySelector(asyncSettings.dataElementId);
                        if (dataElement) {
                            dataElement.innerHTML = data[asyncSettings.dataKey];
                        }

                        // Add modalForm to trigger element after async page update
                        if (asyncSettings.addModalFormFunction) {
                            asyncSettings.addModalFormFunction();
                        }

                        if (asyncSettings.closeOnSubmit) {
                            bootstrap.Modal.getInstance(modal).hide();
                        } else {
                            // Reload form
                            fetch(settings.formURL, {credentials: settings.credentials}).then(res => {
                                return res.text();
                            }).then(data => {
                                let content = modal.querySelector(settings.modalContent);
                                content.innerHTML = data;

                                form = modal.querySelector(settings.modalForm);
                                if (!form) {
                                    console.error('no form present in response')
                                    return;
                                }

                                form.action = settings.formURL;
                                addEventHandlers(modal, form, settings)
                            });
                        }
                    });
                } else if (asyncSettings.closeOnSubmit) {
                    bootstrap.Modal.getInstance(modal).hide();
                }
            });
        }
    }
};

/**
 * Validates given settings/configuration for asynchronous calls.
 *
 * @param {Object} settings Configuration/Settings for associated modal
 * @return {boolean} True if given configuration/settings is valid, false otherwise
 */
const validateAsyncSettings = function (settings) {
    let missingSettings = [];

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
    return missingSettings.length < 1;
};

/**
 * Adds click listener to given button. If button is clicked, associated
 * modal makes a call to given URL("formURL") to load its inner HTML.
 *
 * credentials:
 *      Prevent browser to share credentials (Cookies, Authorization headers & TLS client certificates for future
 *      authentication) secrets with malicious 3rd parties. Defaults to "same-origin".
 *      @see https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#sending_a_request_with_credentials_included
 *
 * @param {HTMLElement} trigger_btn Button that triggers the modal to open/close
 * @param {Object} settings Configuration/Settings for this given modal
 * @return {HTMLElement} The button with an event listener
 */
const modalForm = function (trigger_btn, settings) {
    let defaults = {
        modalID: '#modal',
        modalContent: '.modal-content',
        modalForm: '.modal-content form',
        formURL: null,
        isDeleteForm: false,
        errorClass: 'is-invalid',
        asyncUpdate: false,
        asyncSettings: {
            closeOnSubmit: false,
            successMessage: null,
            dataUrl: null,
            dataElementId: null,
            dataKey: null,
            addModalFormFunction: null
        },
        credentials: 'same-origin',
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        headers: {
            'Content-Type': 'application/json'
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer'
    };

    const replenished_settings = {...defaults, ...settings}

    trigger_btn.addEventListener('click', () => {
        modalFormCallback(replenished_settings);
    })

    return trigger_btn;
}