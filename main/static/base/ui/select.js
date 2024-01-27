document.addEventListener('DOMContentLoaded', () => {
    const selects = document.getElementsByClassName('ui-select');

    for (let select of selects) {
        let button = select.querySelector('span');
        button.addEventListener('click', () => select.classList.toggle('active'));

        let options = select.querySelectorAll('div > *.ui-select-option');
        if (options.length == 0) continue;

        let selector = button.querySelector('span');

        for (let option of options)
            option.addEventListener('click', () => {
                select.classList.remove('active');
                select.dataset.value = option.dataset.value;
                selector.textContent = option.textContent;
            });
    }
});