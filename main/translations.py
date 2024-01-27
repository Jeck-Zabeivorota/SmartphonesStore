from typing import Dict

CHARACTERISTIC_CATEGORIES = {
    'main':         {'ua': 'Головне',           'en': 'Main'},
    'display':      {'ua': 'Дісплей',           'en': 'Display'},
    'connecting':   {'ua': "Зв'язок",           'en': 'Connecting'},
    'memory':       {'ua': "Пам'ять",           'en': 'Memory'},
    'cameras':      {'ua': 'Камери',            'en': 'Cameras'},
    'main_camera':  {'ua': 'Головна камера',    'en': 'Main camera'},
    'front_camera': {'ua': 'Фронтальна камера', 'en': 'Front camera'},
    'processor':    {'ua': 'Процесор',          'en': 'Processor'},
    'dimensions':   {'ua': 'Розміри',           'en': 'Dimensions'},
    'addition':     {'ua': 'Додатково',         'en': 'Addition'},
}

CHARACTERISTIC_ENDINGS = {
    'GHz': {'ua': ' ГГц',    'en': ' GHz'},
    'Gb':  {'ua': ' Гб',     'en': ' Gb'},
    'Mp':  {'ua': ' Мп',     'en': ' Mp'},
    'mAh': {'ua': ' мА*год', 'en': ' mAh'},
    'mm':  {'ua': ' мм',     'en': ' mm'},
    'g':   {'ua': ' г',      'en': ' g'},
}

CHARACTERISTIC_FIELDS = {
    'manufacturer': {'ua': 'Бренд',              'en': 'Manufacturer'},
    'os':           {'ua': 'Операційна система', 'en': 'Operating system'},

    'diagonal':         {'ua': 'Діагональ',                'en': 'Diagonal'},
    'resolution':       {'ua': 'Роздільна здатність',      'en': 'Resolution'},
    'matrix':           {'ua': 'Матриця',                  'en': 'Matrix'},
    'screen_frequency': {'ua': 'Частота оновлення екрану', 'en': 'Screen frequency'},
    'screen_material':  {'ua': 'Матеріал екрану',          'en': 'Screen material'},

    'connection_types': {'ua': "Типи зв'язку",  'en': 'Connection types'},
    'sim_number':       {'ua': 'Кількість SIM', 'en': 'Number of SIM'},
    'sim_size':         {'ua': 'Розмір SIM',    'en': 'SIM size'},

    'ram':               {'ua': "Оперативна пам'ять", 'en': 'RAM'},
    'rom':               {'ua': "Постійна пам'ять",   'en': 'ROM'},
    'additional_memory': {'ua': "Додаткова пам'ять",  'en': 'Additional memory'},
    'max_size_additional_memory': {'ua': "Максимальний розмір додаткової пам'яті", 'en': 'Max size of additional memory'},

    'main_camera':           {'ua': 'Головна камера',              'en': 'Main camera'},
    'number_main_cameras':   {'ua': 'Кількість основних камер',    'en': 'Number of main cameras'},
    'main_camera_features':  {'ua': 'Особливості головної камери', 'en': 'Features of main camera'},
    'main_camera_video':     {'ua': 'Відео головної камери',       'en': 'Main camera video'},
    'main_camera_additions': {'ua': 'Доповнення головної камери',  'en': 'Main camera additions'},

    'front_camera':           {'ua': 'Фронтальна камера',             'en': 'Front camera'},
    'front_camera_video':     {'ua': 'Відео фронтальної камери',      'en': 'Front camera video'},
    'front_camera_additions': {'ua': 'Доповнення фронтальної камери', 'en': 'Front camera additions'},

    'processor':           {'ua': 'Процесор',          'en': 'Processor'},
    'videocore':           {'ua': 'Відеоядро',         'en': 'Videocore'},
    'number_cores':        {'ua': 'Кількість ядер',    'en': 'Number of cores'},
    'processor_frequency': {'ua': 'Частота процесора', 'en': 'Processor frequency'},

    'weight': {'ua': 'Вага',    'en': 'Weight'},
    'width':  {'ua': 'Ширина',  'en': 'Width'},
    'height': {'ua': 'Висота',  'en': 'Height'},
    'depth':  {'ua': 'Глибина', 'en': 'Depth'},

    'battery_volume': {'ua': 'Ємність акумулятора',   'en': 'Battery volume'},
    'wirelesses':     {'ua': 'Бездротові технології', 'en': 'Wirelesses'},
    'connectors':     {'ua': "Роз'єми",     'en': 'Connectors'},
    'security':       {'ua': 'Безпека',     'en': 'Security'},
    'protection':     {'ua': 'Захист',      'en': 'Protection'},
    'sensors':        {'ua': 'Сенсори',     'en': 'Sensors'},
    'features':       {'ua': 'Особливості', 'en': 'Features'},
    'additions':      {'ua': 'Додатково',   'en': 'Additions'},
}

CHARACTERISTIC_CHOICES = {
    'main_camera_features': {
        'autofocus':     {'ua': 'Автофокус',                 'en': 'Autofocus'},
        'video4k':       {'ua': 'Підтримання знімання 4К',   'en': '4K shooring support'},
        'flash':         {'ua': 'Спалах',                    'en': 'Flash'},
        'stabilization': {'ua': 'Стабілізація',              'en': 'Stabilization'},
        'telephotolens': {'ua': "Телеоб'єктив",              'en': 'Telephoto lens'},
        'wideanglelens': {'ua': "Широкутний об'єктив",       'en': 'Wide angle lens'},
        'ultrawidelens': {'ua': "Ультраширокутний об'єктив", 'en': 'Ultra wide angle lens'},
    },
    'wirelesses': {
        'bluetooth':        {'ua': 'Bluetooth',           'en': 'Bluetooth'},
        'nfc':              {'ua': 'NFC',                 'en': 'NFC'},
        'wifi':             {'ua': 'Wi-Fi',               'en': 'Wi-Fi'},
        'infraded port':    {'ua': 'Інфрачервоний порт',  'en': 'Infraded port'},
        'wireless charger': {'ua': 'Безпровідна зарядка', 'en': 'Wireless charger'},
    },
    'security': {
        'faceid':      {'ua': 'Сканнер облича',         'en': 'Face-ID'},
        'fingerprint': {'ua': 'Сканер відбитка пальця', 'en': 'Fingerprint'},
    },
    'features': {
        'flashlight':        {'ua': 'Фонарик',          'en': 'Flashlight'},
        'rounded edges':     {'ua': 'Заокруглені краї', 'en': 'Rounded edges'},
        'thermal imager':    {'ua': 'Тепловізор',       'en': 'Thermal imager'},
        'folds up':          {'ua': 'Складний',         'en': 'Folds up'},
        'waterproof':        {'ua': 'Водонепронекний',  'en': 'Waterproof'},
        'removable battery': {'ua': 'Знімна батарея',   'en': 'Removable battery'},
        'armored':           {'ua': 'Броньований',      'en': 'Armored'},
    },
}

ORDER_STATUS = {
    'is confirmed': {'ua': 'Підтвержується', 'en': 'Is confirmed'},
    'on the way':   {'ua': 'В дорозі',       'en': 'On the way'},
    'arrived':      {'ua': 'Доставлений',    'en': 'Arrived'},
    'canceled':     {'ua': 'Відмінений',     'en': 'Canceled'},
}


def select_labels_by_lang(labels:Dict[str, Dict[str,str]], lang:str) -> Dict[str,str]:
    lang_labels = {}

    for key in labels.keys():
        lang_labels[key] = labels[key][lang]

    return lang_labels

LAYOUT_LABELS = {
    'home' :      {'ua': 'Головна', 'en': 'Home'},
    'products' :  {'ua': 'Товари',  'en': 'Products'},
    'faq' :       {'ua': 'Питання', 'en': 'FAQ'},

    'account' :   {'ua': 'Кабінет',    'en': 'Account'},
    'cart' :      {'ua': 'Кошик',      'en': 'Cart'},
    'orders' :    {'ua': 'Замовлення', 'en': 'Orders'},
    'favorites' : {'ua': 'Улюблені',   'en': 'Favorites'},
    'browsed' :   {'ua': 'Переглянуті товари', 'en': 'Browsed products'},
    'exit' :      {'ua': 'Вихід',      'en': 'Exit'},
    'sing_in' :   {'ua': 'Ввійти',     'en': 'Sing in'},

    'questions':  {'ua': 'Питання', 'en': 'FAQ'},
    'contacts':   {'ua': 'Контакти','en': 'Contacts'},
    'question1':  {'ua': 'Як проходить процес замовлення?', 'en': 'How does the ordering process work?'},
    'question2':  {'ua': 'Які надаються гарантії?',         'en': 'What warranties are provided?'},
    'question3':  {'ua': 'Що таке ID товару?',              'en': 'What is ID of product?'},
}

HOME_LABELS = {
    'hero1': {'ua': 'ВІДКРИЙ ',   'en': 'DISCOVER '},
    'hero2': {'ua': 'ДЛЯ СЕБЕ',   'en': 'WORLD'},
    'hero3': {'ua': ' СВІТ',      'en': ' OF'},
    'hero4': {'ua': 'СМАРТФОНІВ', 'en': 'SMARTPHONES'},

    'top_products':  {'ua': 'КРАЩІ ТОВАРИ',     'en': 'TOP PRODUCTS'},
    'new':           {'ua': 'Нові',             'en': 'New'},
    'discount':      {'ua': 'Знижка',           'en': 'Discount'},
    'more_products': {'ua': 'Більше продуктів', 'en': 'More products'},

    'why_we': {'ua': 'ЧОМУ МИ',                    'en': 'WHY WE'},
    'sells':  {'ua': 'Задоволених клієнтів',       'en': 'Happy sients and sell smartphones'},
    'time':   {'ua': 'Років на ринку',             'en': 'Years on the market'},
    'return': {'ua': 'Клієнтів повернулися знову', 'en': 'Of returning sients'},

    'about_us': {'ua': 'ПРО НАС', 'en': 'ABOUT US'},
    'about_us_desc1': {
        'ua': 'Ми – команда ентузіастів, захоплених світом сучасних технологій. Наш магазин створений для тих, хто шукає надійні та сучасні смартфони за доступними цінами. Поєднуючи якість та функціональність, ми гарантуємо, що ви знайдете ідеальний смартфон для своїх потреб.',
        'en': 'We are a team of enthusiasts passionate about the world of modern technologies. Our store is designed for those seeking reliable and modern smartphones at affordable prices. By combining quality and functionality, we guarantee that you will find the perfect smartphone to meet your needs.',
    },
    'about_us_desc2': {
        'ua': 'Ми пишаємось тим, що наш магазин став частиною вашого шляху у світі технологій, і сподіваємось стати вашим надійним партнером на довгі роки!',
        'en': 'We take pride in our store becoming a part of your journey in the world of technology, and we hope to become your reliable partner for many years to come!',
    },
}

AUTH_LABELS = {
    'login':    {'ua': 'Вхід',       'en': 'Login'},
    'register': {'ua': 'Реєстрація', 'en': 'Register'},
    'name':     {'ua': "Ім'я",       'en': 'Name'},
    'phone':    {'ua': 'Телефон',    'en': 'Phone'},
    'email':    {'ua': 'Емаїл',      'en': 'Email'},
    'password': {'ua': 'Пароль',     'en': 'Password'},
    'repeat_password': {'ua': 'Повторіть пароль', 'en': 'Repeat password'},
}

PRODUCTS_LABELS = {
    'filters':  {'ua': 'Фільтри',   'en': 'Filters'},
    'search':   {'ua': 'Пошук',     'en': 'Search'},
    'sort':     {'ua': 'Сортувати', 'en': 'Sort'},
    'discount': {'ua': 'Знижка',    'en': 'Discount'},

    'by_rating': {'ua': 'по рейтингу', 'en': 'by rating'},
    'from_c2e':  {'ua': 'від дешевих', 'en': 'from cheap'},
    'from_e2c':  {'ua': 'від дорогих', 'en': 'from expensive'},
    'by_date':   {'ua': 'по даті',     'en': 'by date'},

    'not_found':   {'ua': 'Товари не знайдені', 'en': 'Products not found'},
    'browsed':     {'ua': 'Переглянуті товари', 'en': 'Browsed products'},
    'all_history': {'ua': 'Повна історія',      'en': 'All history'},
}

PRODUCT_LABELS = {
    'feedbacks_title': {'ua': 'відгуків',         'en': 'feedbacks'},
    'items_title':     {'ua': 'штук',             'en': 'items'},
    'color':           {'ua': 'Колір',            'en': 'Color'},
    'quantity':        {'ua': 'Кількість',        'en': 'Quantity'},
    'add_to_cart':     {'ua': 'Додати до кошика', 'en': 'Add to cart'},
    'order_now':       {'ua': 'Замовити зараз',   'en': 'Order now'},
    'characters':      {'ua': 'Характеристики',   'en': 'Characters'},
    'feedbacks':       {'ua': 'Відгуки',          'en': 'Feedbacks'},
    'date_of_issue':   {'ua': 'Дата випуску',     'en': 'Date of issue'},
    'my_feedback':     {'ua': 'Мій відгук',       'en': 'My feedback'},
    'save_feedback':   {'ua': 'Зберегти відгук',  'en': 'Save feedback'},
    'no_feedbacks':    {'ua': 'Відгуки відсутні', 'en': 'No feedbacks'},
    'unknowlange':     {'ua': 'Невідомий',        'en': 'Unknowlange'},
}

FAQ_LABELS = {
    'do_you_have_a_question':  {'ua': 'МАЄТЕ ПИТАННЯ?', 'en': 'DO YOU HAVE A QUESTIONS?'},
    'purchase': {'ua': 'Придбання', 'en': 'Purchase'},
    'deliver':  {'ua': 'Доставка',  'en': 'Deliver'},
    'other':    {'ua': 'Інше',      'en': 'Other'},
}

SIDEMENU_LABELS = {
    'info':      {'ua': 'Інформація', 'en': 'Information'},
    'cart':      {'ua': 'Кошик',      'en': 'Cart'},
    'orders':    {'ua': 'Замовлення', 'en': 'Orders'},
    'favorites': {'ua': 'Улюблені',   'en': 'Favorites'},
    'browsed' :  {'ua': 'Переглянуті товари', 'en': 'Browsed products'},
}

USER_INFO_LABELS = {
    'user_data': {'ua': 'Дані користувача', 'en': 'User data'},
    'name':      {'ua': "Ім'я",             'en': 'Name'},
    'email':     {'ua': 'Емаїл',            'en': 'Email'},
    'phone':     {'ua': 'Телефон',          'en': 'Phone'},
    'save_data': {'ua': 'Зберегти дані',    'en': 'Save data'},

    'password':         {'ua': 'Пароль',           'en': 'Password'},
    'current_password': {'ua': 'Поточний пароль',  'en': 'Current password'},
    'new_password':     {'ua': 'Новий пароль',     'en': 'New password'},
    'repeat_password':  {'ua': 'Повторіть пароль', 'en': 'Repeat password'},
    'save_password':    {'ua': 'Зберегти пароль',  'en': 'Save password'},

    'address': {'ua': 'Адреса', 'en': 'Address'},
    'city':    {'ua': 'Місто',  'en': 'City'},
    'street':  {'ua': 'Вулиця', 'en': 'Street'},
    'index':   {'ua': 'Індекс', 'en': 'Index'},
    'save_address': {'ua': 'Зберегти адресу', 'en': 'Save address'},
}

ITEMS_LABELS = {
    'items':          {'ua': 'штук',               'en': 'items'},
    'selected':       {'ua': 'виділено',           'en': 'selected'},
    'not_found':      {'ua': 'Товари не знайдені', 'en': 'Products not found'},
    'color':          {'ua': 'Колір',              'en': 'Color'},
    'total':          {'ua': 'Всього',             'en': 'Total'},
    'selected_title': {'ua': 'товрів вибрано',     'en': 'products selected'},
    'order':          {'ua': 'Замовити',           'en': 'Order'},
    'status':         {'ua': 'статус',             'en': 'status'},
    'date_of_view':   {'ua': 'Дата перегляду',     'en': 'Date of view'},
}


AUTH_MSG = {
    'invalid_value':      {'ua': 'Введено не допустиме значення',         'en': 'Entered invalid value'},
    'email_not_found':    {'ua': 'Користувача з таким email не знайдено', 'en': 'User with this email was not found'},
    'incorrect_password': {'ua': 'Невірний пароль',                       'en': 'Incorrect password'},
    'user_is_auth':       {'ua': 'Користувач автентифікований',           'en': 'User is authenticated'},
    'name_out_of_range':  {
        'ua': "Ім'я повинне містити від 3 до 20 символів",
        'en': 'The name must contain from 3 to 20 characters'
    },
    'incorrect_email':    {'ua': 'Невірний формат email',                 'en': 'Incorrect email format'},
    'email_exists':       {'ua': 'Користувач з таким email вже існує',    'en': 'User with this email already exists'},
    'phone_out_of_range': {
        'ua': 'Номер телефону повинен містити від 7 до 12 цифр',
        'en': 'The phone number must contain from 7 to 12 digits'
    },
    'phone_not_digits':   {'ua': 'Номер телефону має складатися з цифр',  'en': 'Phone number must consist of numbers'},
    'password_out_of_range': {
        'ua': 'Пароль повинен містити від 6 до 100 символів',
        'en': 'The password must contain from 6 to 100 characters'
    },
    'user_registered':    {'ua': 'Користувача зараєстровано',             'en': 'User is registered'},
    'password_mismatch':  {'ua': 'Паролі не збіглися',                    'en': 'Password mismatch'},
}

USER_DATA_MSG = {
    'info_saved': {'ua': 'Інформація збережена', 'en': 'Information saved'},
    'password_saved': {'ua': 'Пароль збережений', 'en': 'Password saved'},
    'address_saved': {'ua': 'Адреса збережена', 'en': 'Address saved'},
    'is_empty': {'ua': 'Поле порожнє', 'en': 'Field is empty'},
    'invalid_character': {'ua': 'Недопустимий символ ";;"', 'en': 'Invalid character ";;"'},
    'city_street_out_of_range': {
        'ua': 'Довжина назви міста та вулиці має бути більше 2 символів',
        'en': 'City and street length must be more than 2 characters'
    },
    'index_not_digits': {'ua': 'Індекс має складатися з цифр', 'en': 'Index must consist of numbers'},
    'address_out_of_range': {
        'ua': 'Довжина адреси перевищує ліміт символів',
        'en': 'Address length exceeds characters limit'
    },
}

PRODUCTS_MSG = {
    'favorites_add': {'ua': 'Додано до улюблених', 'en': 'Added to favorites'},
    'favorites_remove': {'ua': ' товарів видалено із улюблених', 'en': ' products removed from favorites'},
    'cart_add': {'ua': 'Додано до кошика', 'en': 'Added to cart'},
    'cart_remove': {'ua': ' товарів видалено із кошика', 'en': ' products removed from cart'},
    'orders_add': {'ua': 'Замовлення створено', 'en': 'Order is created'},
    'orders_cancel': {'ua': ' замовлень скасовано', 'en': ' orders canceled'},
    'orders_remove': {'ua': ' замовлень видалено', 'en': ' orders removed'},
    'browsed_remove': {'ua': ' товарів видалено із переглянутих товарів', 'en': ' products removed from browsed products'},
    'feedback_saved': {'ua': 'Відгук збережено', 'en': 'Feedback saved'},
}