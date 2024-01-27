function setProductActionEvents(product) {
    const productID = parseInt(product.dataset.product_id);
    const cartButton = product.querySelector('.product-actions-cart');
    const favoriteButton = product.querySelector('.product-actions-favorite');
    const cartCountIndicator = document.querySelector('.menu-cart-products_count');

    product.addEventListener('click', () => window.location.href = PRODUCT_PATH.concat('?id=', productID));

    let errorFunc = (_xhr, status, data) => {
        if (status == 401)
            window.location.href = AUTH_PATH;
        else
            showMsg(data.error, 'error')
    };

    cartButton.addEventListener('click', (event) => {
        if (cartButton.classList.contains('active')) {
            window.open(CART_PATH, '_blank');
            event.stopPropagation();
            return;
        }

        ajax({
            url: API_PRODUCT_PATH,
            method: 'POST',
            headers: {'X-CSRFToken': getCSRFToken()},
            data: {'action': 'cart_add', 'product_id': productID, 'color': 'null', 'quantity': 1},
            success: (data) => {
                cartButton.src = getIcon('check.svg');
                cartButton.classList.add('active');
                cartCountIndicator.classList.add('active');
                cartCountIndicator.textContent = data.count;
            },
            error: errorFunc
        })

        event.stopPropagation();
    });
    favoriteButton.addEventListener('click', (event) => {
        let params;
        if (favoriteButton.classList.contains('active'))
            params = {'action': 'favorite_remove', 'ids': [productID]};
        else
            params = {'action': 'favorite_add', 'product_id': productID};

        ajax({
            url: API_PRODUCT_PATH,
            method: 'POST',
            headers: {'X-CSRFToken': getCSRFToken()},
            data: params,
            success: (data) => {
                if (data.message.startsWith('1')) {
                    favoriteButton.src = getIcon('favorite.svg');
                    favoriteButton.classList.remove('active');
                }
                else {
                    favoriteButton.src = getIcon('favorite_active.svg');
                    favoriteButton.classList.add('active');
                }
            },
            error: errorFunc
        })

        event.stopPropagation();
    });
}

function createHTMLProduct(id, name, photoURL, price, rating, discount, discountPrice, isFavorite, isInCart) {
    const container = createHTMLElement('div', {
        'class': 'product', 'data-product_id': id
    });

    const discountLabel = discount != null ? `<span class="product-discount">${discount}</span>` : '';
    container.appendChild(createHTMLElement('div',
        {'class': 'product-photo_wrap'},
        `${discountLabel}<img src="${photoURL}" alt="Photo">`
    ));

    const cartIcon = getIcon(isInCart ? 'check.svg' : 'cart.svg');
    const favoriteIcon = getIcon(isFavorite ? 'favorite_active.svg' : 'favorite.svg');
    container.appendChild(createHTMLElement('div',
        {'class': 'product-actions'},
        `<img class="product-actions-cart" src="${cartIcon}" alt="Add to cart">` +
        `<img class="product-actions-favorite" src="${favoriteIcon}" alt="Add to favorite">`
    ));

    container.appendChild(createHTMLElement('div', {'class': 'product-name'}, name));

    const priceLabel = discountPrice != null ?
        `${discountPrice} \$ <span class="product-old-price">${price} \$</span>` :
        `${price} \$`;
    const ratingIcon = getIcon('star.svg');
    container.appendChild(createHTMLElement('div',
        {'class': 'product-second'},
        `<b>${priceLabel}</b>` +
        `<div class="product-rating"><img src="${ratingIcon}" alt="Rating"><span>${rating}/5</span></div>`
    ));

    setProductActionEvents(container);

    return container;
}

document.addEventListener('DOMContentLoaded', () => {
    const products = document.getElementsByClassName('product');
    for (let product of products) setProductActionEvents(product);
});