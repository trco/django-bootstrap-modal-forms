/*
django-bootstrap-modal-forms
version : 3.0.4
Copyright (c) 2023 Marcel Rupp
*/

// Open modal & load the form at formURL to the modalContent element
const modalFormCallback = function (settings) {
    let modal = document.querySelector(settings.modalID);
    let content = modal.querySelector(settings.modalContent);

    let modalInstance = bootstrap.Modal.getInstance(modal);
    if (modalInstance === null) {
        modalInstance = new bootstrap.Modal(modal, {
            keyboard: false
        })
    }

    fetch(settings.formURL).then(res => {
        return res.text();
    }).then(data => {
        content.innerHTML = data;
    }).then(() => {
        modalInstance.show();

        let form = modal.querySelector(settings.modalForm);
        if (form) {
            form.setAttribute("action", settings.formURL);
            addEventHandlers(modal, form, settings)
        }
    });
};

const addEventHandlers = function (modal, form, settings) {
    form.addEventListener('submit', (event) => {
        if (settings.isDeleteForm === false) {
            event.preventDefault();
            isFormValid(settings, submitForm);
            return false;
        }
    });

    modal.addEventListener('hidden.bs.modal', (event) => {
        let content = modal.querySelector(settings.modalContent);
        while (content.lastChild) {
            content.removeChild(content.lastChild);
        }
    });
};

// Check if form.is_valid() & either show errors or submit it via callback
const isFormValid = function (settings, callback) {
    let modal = document.querySelector(settings.modalID);
    let form = modal.querySelector(settings.modalForm);
    const headers = new Headers();
    headers.append('X-Requested-With', 'XMLHttpRequest');

    let btnSubmit = modal.querySelector('button[type="submit"]');
    btnSubmit.disabled = true;
    fetch(form.getAttribute("action"), {
        headers: headers,
        method: form.getAttribute("method"),
        body: new FormData(form),
    }).then(res => {
        return res.text();
    }).then(data => {
        if (data.includes(settings.errorClass)) {
            modal.querySelector(settings.modalContent).innerHTML = data;

            form = modal.querySelector(settings.modalForm);
            if (!form) {
                console.error('no form present in response')
                return;
            }

            form.setAttribute("action", settings.formURL);
            addEventHandlers(modal, form, settings)
        } else {
            callback(settings);
        }
    });
};

// Submit form callback function
const submitForm = function (settings) {
    let modal = document.querySelector(settings.modalID);
    let form = modal.querySelector(settings.modalForm);

    if (!settings.asyncUpdate) {
        form.submit();
    } else {
        let asyncSettingsValid = validateAsyncSettings(settings.asyncSettings);
        if (asyncSettingsValid) {
            let asyncSettings = settings.asyncSettings;
            // Serialize form data
            let formData = new FormData(form);
            // Add asyncUpdate and check for it in save method of CreateUpdateAjaxMixin
            formData.append("asyncUpdate", "True");

            fetch(form.getAttribute("action"), {
                method: form.getAttribute("method"),
                body: formData,
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
                    fetch(asyncSettings.dataUrl).then(res => res.json()).then(data => {
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
                            fetch(settings.formURL).then(res => {
                                return res.text();
                            }).then(data => {
                                let content = modal.querySelector(settings.modalContent);
                                content.innerHTML = data;

                                form = modal.querySelector(settings.modalForm);
                                if (!form) {
                                    console.error('no form present in response')
                                    return;
                                }

                                form.setAttribute("action", settings.formURL);
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

const validateAsyncSettings = function (settings) {
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

const modalForm = function(elem, options) {
    // Default settings
    let defaults = {
        modalID: "#modal",
        modalContent: ".modal-content",
        modalForm: ".modal-content form",
        formURL: null,
        isDeleteForm: false,
        errorClass: "is-invalid",
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

    let settings = {...defaults, ...options}

    elem.addEventListener('click', () => {
        modalFormCallback(settings);
    })

    return elem;
}
