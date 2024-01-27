/**
 * Calls a defined callback function on each element of an `arr`, and returns an array that contains the results
 * @param {Array} arr
 * @param {Function} predicate
 * @returns {Array}
*/
function map(arr, predicate) {
    const newArr = new Array(arr.length);
    for (let i = 0; i < arr.length; i++)
        newArr[i] = predicate(arr[i]);
    return newArr;
}

/**
 * Returns CSRF token from field from document
 * @returns {string}
*/
function getCSRFToken() {
    return document.querySelector('input[name=csrfmiddlewaretoken]').value;
}

/**
 * Returns parameters from `url`
 * @param {string} url
 * @returns {{}}
*/
function getURLParams(url) {
    const separIdx = url.indexOf('?');
    if (separIdx == -1) return {};

    const paramsStrList = url.substring(separIdx + 1).split('&');
    const params = {};

    for (const paramStr of paramsStrList)
        if (paramStr.indexOf('=') != -1) {
            const keyValue = paramStr.split('=');
            params[decodeURIComponent(keyValue[0])] = decodeURIComponent(keyValue[1]);
        }
        else params[decodeURIComponent(paramStr)] = '';

    return params;
}

/**
 * Convert json `data` to string with URL parameters
 * @param {{}} data
 * @returns {string}
*/
function jsonToURLParams(data) {
    return Object.keys(data).map((key) => {
        const param = encodeURIComponent(key);

        if (data[key] != null) {
            if (data[key] instanceof Array) {
                const list = Object.values(data[key]).map((value) => encodeURIComponent(value));
                param = param.concat('=', list.join(','));
            }
            else param = param.concat('=', encodeURIComponent(data[key]));
        }

        return param;
    }).join('&');
}

/**
 * Make AJAX request
 * @param {string} url - `string`
 * @param {string} method - `string`
 * @param {{}} headers - `{}?`
 * @param {{}} data - `{}?`
 * @param {Function} success - `Function?`
 * @param {Function} error - `Function?`
*/
function ajax({url, method, headers=null, data=null, success=null, error=null}) {
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if (xhr.status == 200)
                success?.(JSON.parse(xhr.responseText));
            else if (xhr.status == 500)
                error?.(xhr, xhr.status, {error: 'Server error'})
            else 
                error?.(xhr, xhr.status, JSON.parse(xhr.responseText))
        }
    };

    if (method == 'GET' && data != null)
        xhr.open(method, url.concat('?', jsonToURLParams(data)), true);
    else
        xhr.open(method, url, true);

    Object.keys(headers).forEach((key, _i, _keys) =>
        xhr.setRequestHeader(key, headers[key])
    );

    if (method != 'GET' && data != null) {
        xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
        xhr.send(JSON.stringify(data));
    }
    else xhr.send();
}

/**
 * Create and returns HTML element
 * @param {string} name
 * @param {{}} attributs
 * @param {string} content
 * @returns {element}
*/
function createHTMLElement(name, attributs=null, content=null) {
    const element = document.createElement(name);

    if (attributs != null)
        for (let attr in attributs)
            element.setAttribute(attr, attributs[attr]);
    
    element.innerHTML = content;

    return element;
}

/**
 * Show message on page
 * @param {string} message
 * @param {string} type - `[info, error, success, warning]`
*/
function showMsg(message, type) {
    colors = {
        info: '0, 95, 165',
        error: '255, 0, 65',
        success: '0, 135, 50',
        warning: '210, 180, 55',
    }
    const msg = document.getElementById('msg');
    msg.querySelector('.msg-content').textContent = message;
    msg.style.setProperty('--color', colors[type]);
    msg.classList.add('active');
}

function msgEvent() {
    const msg = document.getElementById('msg');
    const msgCloseButton = document.querySelector('#msg .msg-close_button');

    msgCloseButton.addEventListener('click', () => msg.classList.remove('active'));
}

document.addEventListener('DOMContentLoaded', () => {
    msgEvent();
});