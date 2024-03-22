let emailForRecovery = null

function sendData(data, sucess = null) {
    ajax({
        url: API_AUTH_PATH,
        method: 'POST',
        headers: {'X-CSRFToken': getCSRFToken()},
        data: data,
        success: sucess == null ? (_data) => document.location = HOME_PATH : sucess,
        error: (_xhr, _status, data) => showMsg(data['error'], 'error'),
    });
}

function switchForm(form) {
    document.querySelectorAll('#auth-section > .form').forEach((form, _k, _p) =>
        form.classList.remove('active'));

    form.classList.add('active');
}

function linksEvents() {
    const registerForm = document.querySelector('.auth-register');
    const loginForm = document.querySelector('.auth-login');
    const sendCodeForm = document.querySelector('.auth-send_code');

    document.querySelectorAll('.login_link').forEach((link, _k, _p) =>
        link.addEventListener('click', () => switchForm(loginForm)));

    document.querySelector('.register_link').addEventListener('click', () =>
        switchForm(registerForm));
    
    document.querySelector('.recovery_link').addEventListener('click', () =>
        switchForm(sendCodeForm));
}

function loginSubmitEvent() {
    document.querySelector('.auth-login-submit').addEventListener('click', () => {
        const email    = document.querySelector('.auth-login > .email_field').value;
        const password = document.querySelector('.auth-login > .password_field').value;

        sendData({'action': 'login', 'email': email, 'password': password});
    });
}

function registerSubmitEvent() {
    document.querySelector('.auth-register-submit').addEventListener('click', () => {
        const name      = document.querySelector('.auth-register > .name_field').value;
        const email     = document.querySelector('.auth-register > .email_field').value;
        const phone     = document.querySelector('.auth-register > .phone_field').value;
        const password  = document.querySelector('.auth-register > .password_field').value;
        const repeat_password = document.querySelector('.auth-register > .repeat_password_field').value;

        sendData({
            'action': 'register',
            'name': name,
            'email': email,
            'phone': phone,
            'password': password,
            'repeat_password': repeat_password
        });
    });
}

function sendCodeSubmitEvent() {
    document.querySelector('.auth-send_code-submit').addEventListener('click', () => {
        emailForRecovery = document.querySelector('.auth-send_code > .email_field').value;

        sendData(
            {'action': 'send_code', 'email': emailForRecovery },
            (data) => {
                showMsg(data['message'], 'info');
                switchForm(document.querySelector('.auth-change_pass'));
            }
        );
    });
}

function changePasswordSubmitEvent() {
    document.querySelector('.auth-change_pass-submit').addEventListener('click', () => {
        const code      = document.querySelector('.auth-change_pass > .code_field').value.split(' ').join('');
        const password  = document.querySelector('.auth-change_pass > .password_field').value;
        const repeat_password = document.querySelector('.auth-change_pass > .repeat_password_field').value;

        sendData({
            'action': 'change_password',
            'email': emailForRecovery,
            'code': code,
            'password': password,
            'repeat_password': repeat_password
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    linksEvents();

    loginSubmitEvent();
    registerSubmitEvent();
    sendCodeSubmitEvent();
    changePasswordSubmitEvent();
});