function sentData(data) {
    ajax({
        url: API_AUTH_PATH,
        method: 'POST',
        headers: {'X-CSRFToken': getCSRFToken()},
        data: data,
        success: (_data) => document.location = HOME_PATH,
        error: (_xhr, _status, data) => showMsg(data['error'], 'error'),
    });
}

function linksEvents() {
    const registerForm = document.querySelector('.auth-register');
    const loginForm = document.querySelector('.auth-login');
    const registerLink = document.querySelector('.auth-login-register_link');
    const loginLink = document.querySelector('.auth-register-login_link');

    registerLink.addEventListener('click', () => {
        registerForm.classList.add('active');
        loginForm.classList.remove('active');
    });
    loginLink.addEventListener('click', () => {
        loginForm.classList.add('active');
        registerForm.classList.remove('active');
    });
}

function loginSubmitEvent() {
    const submit = document.querySelector('.auth-login-submit');
    submit.addEventListener('click', () => {
        const email    = document.querySelector('.auth-login > .email_field').value;
        const password = document.querySelector('.auth-login > .password_field').value;

        sentData({'action': 'login', 'email': email, 'password': password})
    });
}

function registerSubmitEvent() {
    const submit = document.querySelector('.auth-register-submit');
    submit.addEventListener('click', () => {
        const name      = document.querySelector('.auth-register > .name_field').value;
        const email     = document.querySelector('.auth-register > .email_field').value;
        const phone     = document.querySelector('.auth-register > .phone_field').value;
        const password  = document.querySelector('.auth-register > .password_field').value;
        const repeat_password = document.querySelector('.auth-register > .repeat_password_field').value;

        sentData({
            'action': 'register',
            'name': name,
            'email': email,
            'phone': phone,
            'password': password,
            'repeat_password': repeat_password
        })
    });
}

document.addEventListener('DOMContentLoaded', () => {
    linksEvents();
    loginSubmitEvent();
    registerSubmitEvent();
});