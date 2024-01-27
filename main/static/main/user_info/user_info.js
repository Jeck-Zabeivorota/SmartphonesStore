/**
 * Make AJAX request for save data on server
 * @param {{}} data
*/
function saveData(data) {
    ajax({
        url: API_USERDATA_PATH,
        method: 'POST',
        headers: {'X-CSRFToken': getCSRFToken()},
        data: data,
        success: (data) => showMsg(data['message'], 'success'),
        error: (_xhr, _status, data) => showMsg(data['error'], 'error'),
    });
}

function infoSubmitEvent() {
    const submit = document.getElementById('info_submit');
    submit.addEventListener('click', () => {
        const name  = document.getElementById('name_field').value;
        const email = document.getElementById('email_field').value;
        const phone = document.getElementById('phone_field').value;

        saveData({'action': 'change_info', 'name': name, 'email': email, 'phone': phone})
    });
}

function passwordSubmitEvent() {
    const submit = document.getElementById('password_submit');
    submit.addEventListener('click', () => {
        const curr_pass   = document.getElementById('curr_pass_field').value;
        const new_pass    = document.getElementById('new_pass_field').value;
        const repeat_pass = document.getElementById('repeat_pass_field').value;

        saveData({
            'action': 'change_password',
            'current_password': curr_pass,
            'new_password': new_pass,
            'repeat_password': repeat_pass
        })
    });
}

function addressSubmitEvent() {
    const submit = document.getElementById('address_submit');
    submit.addEventListener('click', () => {
        const city  = document.getElementById('city_field').value;
        const street = document.getElementById('street_field').value;
        const index = document.getElementById('index_field').value;

        saveData({'action': 'change_address', 'city': city, 'street': street, 'index': index})
    });
}

document.addEventListener('DOMContentLoaded', () => {
    infoSubmitEvent();
    passwordSubmitEvent();
    addressSubmitEvent();
});