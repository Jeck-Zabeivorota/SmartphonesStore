let filterIsMobil = false;
let filtersContainer, mobilFiltersContainer, filtersBlock;

function createParams(page=null) {
    const params = {'page': page == null ? activePage : page};

    const search_value = document.querySelector('.products-actions-search b').textContent;
    if (search_value != '') params['src'] = search_value;

    const sort = document.querySelector('.products-actions-sort > .ui-select');
    params['sort'] = sort.dataset.value;

    const discount = document.querySelector('.products-actions-discount.active');
    if (discount != null) params['discount'] = null;

    const fieldFilters = document.getElementsByClassName('products-filter-field_filters');

    for (const fieldFilter of fieldFilters) {
        const filters = fieldFilter.querySelectorAll('input:checked');

        if (filters.length == 0) continue;

        params[fieldFilter.dataset.value] = map(filters, (filter) => filter.value);
    }

    return params;
}

function createAndSetPager() {
    const pager = document.querySelector('.product-pager');
    pager.innerHTML = '';

    if (allPages == 1) return;

    const arrow = getIcon('arrow_down_accent.svg');

    if (activePage > 1)
        pager.appendChild(createHTMLElement('img', {
            'class': 'product-pager-preview', 'style': '--angle: 90deg;', 'src': arrow
        }));

    const pages = new Array(9);

    if (allPages <= 9) {
        for (let i = 0; i < allPages; i++)
            pages[i] = i + 1;
    }
    else {
        pages[0] = 1;
        pages[1] = (activePage - 3 > 2) ? '...' : 2;
        pages[8] = (activePage + 3 < allPages - 1) ? '...' : allPages - 1;
        pages[9] = allPages;

        if (pages[1] == 2)
            for (let i = 2; i < 7; i++)
                pages[i] = i + 1;
        
        else if (pages[8] == allPages - 1)
            for (let i = 2; i < 7; i++)
                pages[i] = allPages - (8 - i);
        
        else
            for (let i = 2; i < 7; i++)
                pages[i] = activePage - 2 + (i - 2)
    }

    for (const page of pages) {
        if (page == undefined) break;

        const is_link = page != '...' && page != activePage;
        const item = createHTMLElement('span', is_link ? {'class': 'ui-link'} : null, page);

        if (is_link) item.addEventListener('click', () => downloadProducts(page))
        
        pager.appendChild(item);
    }

    if (activePage < allPages)
        pager.appendChild(createHTMLElement('img', {
            'class': 'product-pager-next', 'style': '--angle:-90deg;', 'src': arrow
        }));
}

function downloadProducts(page=null) {
    const productsList = document.querySelector('.products-list');
    productsList.classList.add('load');

    ajax({
        url: API_PRODUCTS_PATH,
        method: 'GET',
        headers: {'X-CSRFToken': getCSRFToken()},
        data: createParams(page),
        success: (data) => {
            productsList.innerHTML = '';
            const capture = document.querySelector('.products-capture');
            const products = Object.values(data.products);

            if (products.length > 0) {
                products.forEach((product) =>
                productsList.appendChild(createHTMLProduct(
                    product.id,
                    product.name,
                    product.photoURL,
                    product.price,
                    product.rating,
                    product.discount,
                    product.discountPrice,
                    product.is_favorite,
                    product.is_in_cart
                )));
                capture.classList.remove('active');
            }
            else capture.classList.add('active');

            allPages = data.pages.all_pages;
            activePage = data.pages.active_page;
            createAndSetPager();

            productsList.classList.remove('load');
        },
        error: (_xhr, _status, data) => {
            products.classList.remove('load');
            showMsg(data.error, 'error');
        }
    });
}

function filtersEvents() {
    const filters = document.querySelectorAll('.products-filter-field_filters input[type="checkbox"]');

    for (const filter of filters)
        filter.addEventListener('change', () => downloadProducts());
}

function searchEvent() {
    const search = document.querySelector('.products-actions-search');

    search.querySelector('img').addEventListener('click', () => {
        search.classList.remove('active');
        downloadProducts();
    });
}

function sortEvents() {
    const options = document.querySelectorAll('.products-actions-sort > .ui-select > div > .ui-select-option');

    for (const option of options)
        option.addEventListener('click', () => downloadProducts());
}

function discountEvent() {
    const discount = document.querySelector('.products-actions-discount');
    discount.addEventListener('click', () => {
        discount.classList.toggle('active');
        downloadProducts();
    });
}


function setFromParams() {
    const params = getURLParams(window.location.href);

    if ('src' in params) {
        const search = document.querySelector('.products-actions-search');
        search.classList.add('active');
    
        const searchValue = search.querySelector('b');
        searchValue.textContent = params['src'];
    }

    if ('sort' in params) {
        const sort = document.querySelector('.products-actions-sort > .ui-select');
        const option = sort.querySelector(`div > .ui-select-option[data-value="${params['sort']}"]`);

        if (option != null) {
            const selector = sort.querySelector('span > span');
            sort.dataset.value = option.dataset.value;
            selector.textContent = option.textContent;
        }
    }

    if ('discount' in params) {
        const discount = document.querySelector('.products-actions-discount');
        discount.classList.add('active');
    }

    const filters = document.getElementsByClassName('products-filter-field_filters');
    for (const filter of filters) {
        if (!(filter.dataset.value in params)) continue;
        const value = params[filter.dataset.value];
        
        if (value == '') continue;
        const keys = value.split(',');

        const checkboxes = filter.querySelectorAll('input[type="checkbox"]');
        for (const checkbox of checkboxes)
            checkbox.checked = keys.includes(checkbox.value);
    }
}

function checkFilter() {
    if (!filterIsMobil && window.innerWidth <= 700) {
        mobilFiltersContainer.appendChild(filtersBlock);
        filterIsMobil = true;
    }

    else if (filterIsMobil && window.innerWidth > 700) {
        filtersContainer.appendChild(filtersBlock);
        filterIsMobil = false;
    }
}

window.addEventListener('resize', checkFilter);

function mobilFilterEvents() {
    const filterButton = document.querySelector('.products-actions-filter');

    filterButton.addEventListener('click', () => 
        mobilFiltersContainer.classList.toggle('active')
    );

    const mobilFilterCloseBtn = document.querySelector('.products-mobil_filters-close');

    mobilFilterCloseBtn.addEventListener('click', () => 
        mobilFiltersContainer.classList.remove('active')
    );
}

document.addEventListener('DOMContentLoaded', () => {
    // Constants
    filtersContainer = document.querySelector('.products-filters_container');
    mobilFiltersContainer = document.querySelector('.products-mobil_filters_container');
    filtersBlock = document.querySelector('.products-filters_block');
    
    // set data
    setFromParams();
    createAndSetPager();
    checkFilter();

    // Events
    mobilFilterEvents();
    filtersEvents();
    searchEvent();
    sortEvents();
    discountEvent();
});