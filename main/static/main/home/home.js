let menuBackground;
let menuIsOpacity = false;

function check_menu() {
    if (!menuIsOpacity && window.scrollY < 10) {
        menuBackground.classList.add('menu-opacity');
        menuIsOpacity = true;
    }
    else if (menuIsOpacity && window.scrollY > 10) {
        menuBackground.classList.remove('menu-opacity');
        menuIsOpacity = false;
    }
}

function tabsEvents() {
    const tabNew = document.querySelector('.products-tab-new');
    const tabDiscount = document.querySelector('.products-tab-discount');
    const listNew = document.querySelector('.products-new');
    const listDiscount = document.querySelector('.products-discount');

    tabNew.addEventListener('click', () => {
        tabNew.classList.add('active');
        listNew.classList.add('active');
        tabDiscount.classList.remove('active');
        listDiscount.classList.remove('active');
    });

    tabDiscount.addEventListener('click', () => {
        tabDiscount.classList.add('active');
        listDiscount.classList.add('active');
        tabNew.classList.remove('active');
        listNew.classList.remove('active');
    });
}

window.addEventListener('scroll', check_menu);

document.addEventListener("DOMContentLoaded", () => {
    menuBackground = document.querySelector('.menu-background');
    check_menu();
    tabsEvents();
});