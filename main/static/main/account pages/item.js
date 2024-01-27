let is_block = false, is_cart;
const quantityValues = {};

const Messages = {
    'no_selected': {'ua': 'Товари не вибрані',   'en': 'No products selected'},
    'cart_add':    {'ua': ' замовлень створено', 'en': ' orders created'},
}

function setSelectedData() {
    const actions = document.querySelector('.panel-actions'),
          selectedIndicator = actions.querySelector('.panel-actions-selected > span'),
          selectedItems = document.querySelectorAll('.item.active');

    selectedIndicator.textContent = selectedItems.length;

    if (selectedItems.length > 0)
        actions.classList.add('active');
    else
        actions.classList.remove('active');

    if (is_cart) setOrderData(selectedItems);
}

function setOrderData(selectedItems = []) {
    let price = 0;
    for (const item of selectedItems) {
        const quantity = item.querySelector('.item-quantity .ui-counter-value');
        price += parseFloat(item.dataset.price) * parseInt(quantity.value);
    }

    const selectedIndicator = document.querySelector('.order-count > b');
    const totalPrice = document.querySelector('.order-price > b');

    selectedIndicator.textContent = selectedItems.length;
    totalPrice.textContent = price.toFixed(2) + ' $';
}

function setCartProductsCount(count) {
    const counter = document.querySelector('.menu-cart-products_count');

    if (count == 0)
        counter.classList.remove('active');
    else
        counter.classList.add('active');

    counter.textContent = count;
}


function productEvents(items) {
    for (let item of items) {
        let title = item.querySelector('.item-name');
        let image = item.querySelector('img');

        let onClick = () => window.location.href = PRODUCT_PATH.concat('?id=', item.dataset.product_id);

        title.addEventListener('click', onClick);
        image.addEventListener('click', onClick);
    }
}

function cartEvents(items) {
    const element = document.querySelector('.item-actions-cart');
    if (element == null) return;

    const cartCountIndicator = document.querySelector('.menu-cart-products_count');

    for (let item of items) {
        let button = item.querySelector('.item-actions-cart');
        button.addEventListener('click', () => {
            if (is_block) return;
            is_block = true;

            if (button.classList.contains('active')) {
                window.open(CART_PATH, '_blank');
                return;
            }

            ajax({
                url: API_PRODUCT_PATH,
                method: 'POST',
                headers: {'X-CSRFToken': getCSRFToken()},
                data: {
                    'action': 'cart_add',
                    'product_id': parseInt(item.dataset.product_id),
                    'color': 'null',
                    'quantity': 1
                },
                success: (data) => {
                    button.src = getIcon('check.svg');
                    button.classList.add('active');
                    cartCountIndicator.classList.add('active');
                    cartCountIndicator.textContent = data.count;
                    is_block = false;
                },
                error: (_xhr, _status, data) => {
                    showMsg(data.error, 'error');
                    is_block = false;
                }
            });
        });
    }
}

function favoriteEvents(items) {
    const element = document.querySelector('.item-actions-favorite');
    if (element == null) return;

    for (let item of items) {
        let button = item.querySelector('.item-actions-favorite');
        button.addEventListener('click', () => {
            if (is_block) return;
            is_block = true;

            let params;
            const product_id = parseInt(item.dataset.product_id);

            if (button.classList.contains('active'))
                params = {'action': 'favorite_remove', 'ids': [product_id]};
            else
                params = {'action': 'favorite_add', 'product_id': product_id};

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
                    is_block = false;
                },
                error: (_xhr, _status, data) => {
                    showMsg(data.error, 'error');
                    is_block = false;
                }
            });
        });
    }
}

function deleteEvents(items, itemsContainer, itemsCountIndicator, notFoundCapture) {
    const element = itemsContainer.querySelector('.item-actions-delete');
    if (element == null) return;

    for (const item of items)
        item.querySelector('.item-actions-delete').addEventListener('click', () => {
            if (is_block) return;
            is_block = true;

            ajax({
                url: API_PRODUCT_PATH,
                method: 'POST',
                headers: {'X-CSRFToken': getCSRFToken()},
                data: {'action': DELETE_ACTION, 'ids': [parseInt(item.dataset.id)]},
                success: (data) => {
                    itemsContainer.removeChild(item);
                    itemsCountIndicator.textContent = data.count;
                    if (data.count == 0) notFoundCapture.classList.add('active');

                    if (item.classList.contains('active')) setSelectedData();
                    if (is_cart) setCartProductsCount(data.count);

                    showMsg(data.message, 'success');
                    is_block = false;
                },
                error: (_xhr, _status, data) => {
                    showMsg(data.error, 'error');
                    is_block = false;
                }
            });
        });
}

function cancelOrderEvents(items) {
    const element = document.querySelector('.item-actions-cancel');
    if (element == null) return;

    for (const item of items) {
        const button = item.querySelector('.item-actions-cancel');
        if (button.classList.contains('hide')) continue;

        button.addEventListener('click', () => {
            if (is_block) return;
            is_block = true;

            ajax({
                url: API_PRODUCT_PATH,
                method: 'POST',
                headers: {'X-CSRFToken': getCSRFToken()},
                data: {'action': 'order_cancel', 'ids': [parseInt(item.dataset.id)]},
                success: (data) => {
                    showMsg(data.message, 'success');
                    const deleteButton = item.querySelector('.item-actions-delete');
                    const status = item.querySelector('.item-status > b');

                    button.classList.add('hide');
                    deleteButton.classList.remove('hide');
                    status.textContent = data.new_status;
                    status.style.color = `rgb(${data.new_status_color})`;

                    is_block = false;
                },
                error: (_xhr, _status, data) => {
                    showMsg(data.error, 'error');
                    is_block = false;
                }
            });
        });
    }
}

function selectorEvents(items) {
    const element = document.querySelector('.item-selector');
    if (element == null) return;
    
    for (const item of items)
        item.querySelector('.item-selector').addEventListener('click', () => {
            item.classList.toggle('active');
            setSelectedData()
        });
}


function selectorAllEvent(items, actions) {
    const selectorAll = actions.querySelector('.panel-actions-selector');
    const selectedIndicator = actions.querySelector('.panel-actions-selected > span');

    selectorAll.addEventListener('click', () => {
        const unselectedItems = document.querySelectorAll('.item:not(.active)');

        if (unselectedItems.length > 0) {
            for (let item of unselectedItems) item.classList.add('active');
            selectedIndicator.textContent = items.length;
            if (is_cart) setOrderData(items);
        }
        else {
            for (let item of items) item.classList.remove('active');
            selectedIndicator.textContent = '0';
            actions.classList.remove('active');
            if (is_cart) setOrderData();
        }
    });
}

function deleteSelectedEvent(itemsContainer, itemsCountIndicator, actions, notFoundCapture) {
    const button = actions.querySelector('.panel-actions-delete');
    const selectedIndicator = actions.querySelector('.panel-actions-selected > span');

    button.addEventListener('click', () => {
        if (is_block) return;
        is_block = true;

        const selectedItems = document.querySelectorAll('.item.active');
        if (selectedItems.length == 0) return;

        ajax({
            url: API_PRODUCT_PATH,
            method: 'POST',
            headers: {'X-CSRFToken': getCSRFToken()},
            data: {'action': DELETE_ACTION, 'ids': map(selectedItems, (item) => parseInt(item.dataset.id))},
            success: (data) => {
                showMsg(data.message, 'success');

                for (let item of selectedItems) itemsContainer.removeChild(item);
                itemsCountIndicator.textContent = data.count;
                if (data.count == 0) notFoundCapture.classList.add('active');

                selectedIndicator.textContent = '0';
                actions.classList.remove('active');

                if (is_cart) {
                    setOrderData();
                    setCartProductsCount(data.count);
                }

                is_block = false;
            },
            error: (_xhr, _status, data) => {
                showMsg(data.error, 'error');
                is_block = false;
            }
        });
    });
}

function orderEvent(itemsContainer, itemsCountIndicator, notFoundCapture) {
    const button = document.querySelector('.order-order');

    button.addEventListener('click', () => {
        if (is_block) return;
        const selectedItems = itemsContainer.querySelectorAll('.item.active');
        if (selectedItems.length == 0) {
            showMsg(Messages['no_selected'][LANG], 'error');
            return;
        }

        is_block = true;
        let responces = 0;
        const addedOrders = [];

        const complate = (itemsCount) => {
            for (const item of addedOrders) itemsContainer.removeChild(item);

            itemsCountIndicator.textContent = itemsCount;
            if (itemsCount == 0) notFoundCapture.classList.add('active');
            setSelectedData();
            setCartProductsCount(itemsCount);

            showMsg(addedOrders.length + Messages['cart_add'][LANG], 'success');
            is_block = false;
        }

        for (const item of selectedItems) {
            ajax({
                url: API_PRODUCT_PATH,
                method: 'POST',
                headers: {'X-CSRFToken': getCSRFToken()},
                data: {
                    'action': 'order_add',
                    'cart_product_id': parseInt(item.dataset.id),
                    'color': item.dataset.color,
                    'quantity': parseInt(item.dataset.quantity)
                },
                success: (data) => {
                    addedOrders.push(item);
                    if (selectedItems.length == ++responces) complate(data.cart_count);
                },
                error: (_xhr, _status, data) => {
                    showMsg(data.error, 'error');
                    if (selectedItems.length == ++responces) complate(data.cart_count);
                }
            })
        }
    });
}

function quantityEvents(items) {
    for (const item of items) {
        quantityValues[item.dataset.id] = parseInt(item.dataset.quantity);

        const counterIncrement = item.querySelector('.item-quantity .ui-counter-increment'),
              counterDecrement = item.querySelector('.item-quantity .ui-counter-decrement'),
              counterValue     = item.querySelector('.item-quantity .ui-counter-value'),
              all_quantity     = parseInt(item.dataset.all_quantity);

        const updateQuantity = () => {
            ajax({
                url: API_PRODUCT_PATH,
                method: 'POST',
                headers: {'X-CSRFToken': getCSRFToken()},
                data: {
                    'action': 'cart_quantity',
                    'cart_product_id': parseInt(item.dataset.id),
                    'value': quantityValues[item.dataset.id]
                },
                success: (_data) => {
                    counterValue.value = quantityValues[item.dataset.id];
                    if (item.classList.contains('active'))
                        setOrderData(document.querySelectorAll('.item.active'));
                },
                error: (_xhr, _status, data) => showMsg(data.error, 'error')
            });
        };

        counterIncrement.addEventListener('click', () => {
            if (quantityValues[item.dataset.id] < all_quantity) {
                quantityValues[item.dataset.id]++;
                updateQuantity();
            }
        });
        counterDecrement.addEventListener('click', () => {
            if (quantityValues[item.dataset.id] > 1) {
                quantityValues[item.dataset.id]--;
                updateQuantity();
            }
        });
        counterValue.addEventListener('change', () => {
            const value = parseInt(counterValue.value.replace(/[^0-9]/g, ''));

            if (Number.isNaN(value) || value < 1) quantityValues[item.dataset.id] = 1;
            else if (value > all_quantity) quantityValues[item.dataset.id] = all_quantity;
            else quantityValues[item.dataset.id] = value;

            updateQuantity();
        });
    }
}


window.addEventListener('DOMContentLoaded', () => {
    const container       = document.getElementById('items-section'),
          itemsCountIndicator = container.querySelector('.panel-count > span'),
          actions         = container.querySelector('.panel-actions'),
          notFoundCapture = container.querySelector('.not_found_capture'),
          items           = container.getElementsByClassName('item');
    is_cart = document.getElementById('order-section') == null ? false : true;

    productEvents(items);
    cartEvents(items);
    favoriteEvents(items);
    deleteEvents(items, container, itemsCountIndicator, notFoundCapture);
    cancelOrderEvents(items);

    if (actions != null) {
        selectorEvents(items);
        selectorAllEvent(items, actions);
        deleteSelectedEvent(container, itemsCountIndicator, actions, notFoundCapture);
        if (is_cart) {
            orderEvent(container, itemsCountIndicator, notFoundCapture);
            quantityEvents(items);
        }
    }
});