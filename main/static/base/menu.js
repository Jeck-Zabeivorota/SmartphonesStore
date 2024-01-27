function searchEvents() {
    const menuItem = document.querySelector('.menu-search');
    const mobilMenuItem = document.querySelector('.menu-mobil-search');
    const block = document.getElementById('search_block');
    const searchButton = block.querySelector('.search_block-search');
    const closeButton = block.querySelector('.search_block-close');

    menuItem.addEventListener('click', () => block.classList.toggle('active'));
    mobilMenuItem.addEventListener('click', () => block.classList.toggle('active'));
    closeButton.addEventListener('click', () => block.classList.remove('active'));
    searchButton.addEventListener('click', () => {
        const field = block.querySelector('.search_block-field');
        if (field.value != '')
            window.location.href = PRODUCTS_PATH.concat('?src=', encodeURIComponent(field.value));
    });
}

function mobilMenuEvents() {
    const menu = document.querySelector('.menu-mobil-menu');
    const block = document.getElementById('mobil_menu_block');

    menu.addEventListener('click', () => block.classList.toggle('active'));
}

function langEvents() {
    const langs = document.getElementsByClassName('lang');

    for (const lang of langs) {
        lang.addEventListener('click', () => ajax({
            url: API_LANG_PATH,
            method: 'POST',
            headers: {'X-CSRFToken': getCSRFToken()},
            data: {'lang': lang.dataset.lang},
            success: (_data) => document.location.reload(),
            error: (_xhr, _status, data) => showMsg(data['error'], 'error')
        }));
    }
}

document.addEventListener('DOMContentLoaded', () => {
    searchEvents();
    mobilMenuEvents();
    langEvents();
});