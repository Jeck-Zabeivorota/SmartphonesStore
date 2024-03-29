# Технології і залежності

### Back-end:
- Мови программування:
    - python 3.11.7
- Залежності:
    - django 4.0
    - django-multiselectfield 0.1.12

### Front-end:
- Мови программування:
    - HTML & CSS
    - JavaScript
- Залежності: **відсутні**


# Структура і архітектура проекту

За основу взятий паттерн MVC та микросервісна архітектура.
Проект складається з наступних елементів:

### Контроллер:

В ролі контроллера виступає стандартний файл "*main/views.py*", енд-поінти якого розділені на два типи:

**HTML API:** стягують дані для формування html-документу та повертає його в виді відповіді.

**JSON API:** виконують операції в залежності від запиту та повертає відповідь в виді json.

---

### Моделі:

Моделі розділені на два типи:

**Entity:** головна задача цієї моделі надання даних, тому вони повинні містити в собі лише поля з данними та простий функціонал по роботі з ними (наприклад форматування або повернення данних на основі значень з полів). Також ці класи можуть мати статичні методи для додавання нових полів з даними до сутностей типу цього ж класу. Всі сутності зберігаються в файлі "*main/models.py*".

**Service:** класи, які містять в собі комплексну логіку направлену на вирішення певної задачі або групи задач. Більшість сервісів зберігаються в файлі "*main/services.py*", а більш комплекстний сервіс відповідний за обробку продуктів знаходиться в файлі "*main/products_componer.py*".

---

### Додаткові файли:

**Переклади:** словарі з повідомленнями на різних мовах знаходяться в файлі "*main/translations.py*".

**Списки с варіаціями:** списки з варіаціями для полів характеристики продуктів знаходиться в файлі "*main/field_choices.py*".

**Інструменти:** в файлі "*main/tools.py*" знаходяться допоміжні для розробки функції і класи.