let quantity = 1;

const Messages = {
    'color_not_selected':  {'ua': 'Колір не вибраний',       'en': 'Color is not selected'},
    'cart_add':            {'ua': 'Товар доданий до кошика', 'en': 'Product added to cart'},
    'order_add':           {'ua': 'Товар замовлено',         'en': 'Product is order'},
    'rating_not_selected': {'ua': 'Оцінка не указана',       'en': 'Rating is not indicated'},
}

function photosEventsAndScr() {
    const mainPhoto = document.querySelector('.photos-main_photo');
    const photos = document.getElementsByClassName('photos-photo');

    for (let photo of photos)
        if (mainPhoto.src == photo.src) {
            photo.classList.add('active');
            break;
        }

    for (let photo of photos)
        photo.addEventListener('click', () => {
            for (let p of photos) p.classList.remove('active');
            photo.classList.add('active');

            mainPhoto.src = photo.src;
        });
}

function setRating() {
    const rating = document.querySelector('.panel-rating > div');
    const icon = getIcon('star.svg');

    for (let i = 0; i < 5; i++) {
        let opacity = PRODUCT_RATING - i;

        if (opacity < 0.1)
            opacity = 0.1;
        else if (opacity > 1.0)
            opacity = 1.0;
        
        rating.appendChild(createHTMLElement('img', {'src': icon, 'style': `opacity: ${opacity};`}));
    }
}

function colorsEvents() {
    const colors = document.querySelectorAll('.panel-colors > div');

    for (let color of colors)
        color.addEventListener('click', () => {
            if (color.classList.contains('active')) return;
            
            for (let c of colors) c.classList.remove('active');
            color.classList.add('active');
        });
}

function quantityEvents() {
    const counterIncrement = document.querySelector('.panel-quantity .ui-counter-increment'),
          counterDecrement = document.querySelector('.panel-quantity .ui-counter-decrement'),
          counterValue     = document.querySelector('.panel-quantity .ui-counter-value'),
          totalPrice       = document.querySelector('.panel-quantity-price'),
          totalOldPrice    = PRODUCT_DISCOUNT > 0 ? document.querySelector('.panel-quantity-old_price > span') : null;

    const updateQuantity = () => {
        counterValue.value = quantity;
        const price = PRODUCT_PRICE * quantity;

        if (PRODUCT_DISCOUNT == 0)
            totalPrice.textContent = price.toFixed(2) + ' $';
        else {
            totalPrice.textContent = (price - price * PRODUCT_DISCOUNT).toFixed(2) + ' $';
            totalOldPrice.textContent = price.toFixed(2) + ' $';
        }
    };

    counterIncrement.addEventListener('click', () => {
        if (quantity < PRODUCT_QUANTITY) {
            ++quantity;
            updateQuantity();
        }
    });
    counterDecrement.addEventListener('click', () => {
        if (quantity > 1) {
            --quantity;
            updateQuantity();
        }
    });
    counterValue.addEventListener('change', () => {
        const value = parseInt(counterValue.value.replace(/[^0-9]/g, ''));

        if (Number.isNaN(value) || value < 1) quantity = 1;
        else if (value > PRODUCT_QUANTITY) quantity = PRODUCT_QUANTITY;
        else quantity = value;

        updateQuantity();
    });
}

function tabsEvents() {
    const tabs = document.querySelectorAll('.panel-tabs > *');
    const tabViews = document.getElementsByClassName('panel-tabview');

    for (let i = 0; i < tabs.length; i++) {
        tabs[i].addEventListener("click", () =>
        {
            for (let k = 0; k < tabs.length; k++) {
                tabs[k].classList.remove('active');
                tabViews[k].classList.remove('active');
            }
            tabs[i].classList.add('active');
            tabViews[i].classList.add('active');
        });
    }
}

function setUserRating() {
    const rating = document.querySelector('.feedback-form-rating');
    if (rating == null) return;

    const icon = getIcon('star.svg');
    let opacity;

    for (let i = 1; i <= 5; i++) {
        if (!Number.isNaN(user_rating) && user_rating >= i) opacity = 1.0;
        else opacity = 0.1;
        const star = createHTMLElement('img', {'src': icon, 'style': `opacity: ${opacity};`});

        star.addEventListener('click', () => {
            const stars = rating.querySelectorAll('img');
            for (let s of stars) s.style.opacity = 0.1;
            for (let k = 0; k < i; k++) stars[k].style.opacity = 1.0;
            user_rating = i;
        });

        rating.appendChild(star);
    }
}


function addToCartEvent() {
    const button = document.querySelector('.panel-actions-cart');
    const cartCountIndicator = document.querySelector('.menu-cart-products_count');

    button.addEventListener('click', () => {
        const color = document.querySelector('.panel-colors > div.active');

        if (color == null) {
            showMsg(Messages['color_not_selected'][LANG], 'error');
            return;
        }

        ajax({
            url: API_PRODUCT_PATH,
            method: 'POST',
            headers: {'X-CSRFToken': getCSRFToken()},
            data: {
                'action': 'cart_add',
                'product_id': PRODUCT_ID,
                'color': color.dataset.value,
                'quantity': quantity
            },
            success: (data) => {
                showMsg(Messages['cart_add'][LANG], 'success');
                cartCountIndicator.classList.add('active');
                cartCountIndicator.textContent = data.count;
            },
            error: (_xhr, status, data) => {
                if (status == 401)
                    window.location.href = AUTH_PATH;
                else
                    showMsg(data.error, 'error')
            }
        });
    });
}

function addToOrdersEvent() {
    const button = document.querySelector('.panel-actions-order');

    button.addEventListener('click', () => {
        const color = document.querySelector('.panel-colors > div.active');

        if (color == null) {
            showMsg(Messages['color_not_selected'][LANG], 'error');
            return;
        }

        ajax({
            url: API_PRODUCT_PATH,
            method: 'POST',
            headers: {'X-CSRFToken': getCSRFToken()},
            data: {
                'action': 'order_add',
                'product_id': PRODUCT_ID,
                'color': color.dataset.value,
                'quantity': quantity
            },
            success: (_data) => showMsg(Messages['order_add'][LANG], 'success'),
            error: (_xhr, status, data) => {
                if (status == 401)
                    window.location.href = AUTH_PATH;
                else
                    showMsg(data.error, 'error')
            }
        });
    });
}

function addToFavoriteEvent() {
    const button = document.querySelector('.panel-actions-favorite');

    button.addEventListener('click', () => {
        let params;
        if (button.classList.contains('active'))
            params = {'action': 'favorite_remove', 'ids': [PRODUCT_ID]};
        else
            params = {'action': 'favorite_add', 'product_id': PRODUCT_ID};

        ajax({
            url: API_PRODUCT_PATH,
            method: 'POST',
            headers: {'X-CSRFToken': getCSRFToken()},
            data: params,
            success: (data) => {
                if (data.message.startsWith('1')) {
                    button.src = getIcon('favorite.svg');
                    button.classList.remove('active');
                }
                else {
                    button.src = getIcon('favorite_active.svg');
                    button.classList.add('active');
                }
            },
            error: (_xhr, status, data) => {
                if (status == 401)
                    window.location.href = AUTH_PATH;
                else
                    showMsg(data.error, 'error')
            }
        });
    });
}

function saveFeedbackEvent() {
    const button = document.querySelector('.feedback-form-save');
    if (button == null) return;
    const desc = document.querySelector('.feedback-form-desc');

    button.addEventListener('click', () => {
        if (Number.isNaN(user_rating)) {
            showMsg(Messages['rating_not_selected'][LANG], 'error');
            return;
        }

        ajax({
            url: API_FEEDBACK_PATH,
            method: 'POST',
            headers: {'X-CSRFToken': getCSRFToken()},
            data: {
                'product_id': PRODUCT_ID,
                'rating': user_rating,
                'desc': desc.value
            },
            success: (data) => showMsg(data.message, 'success'),
            error: (_xhr, status, data) => {
                if (status == 401)
                    window.location.href = AUTH_PATH;
                else
                    showMsg(data.error, 'error')
            }
        });
    });
}


document.addEventListener('DOMContentLoaded', () => {
    photosEventsAndScr();
    setRating();
    colorsEvents();
    quantityEvents();
    tabsEvents();
    setUserRating();

    addToCartEvent();
    addToOrdersEvent();
    addToFavoriteEvent();
    saveFeedbackEvent();
});