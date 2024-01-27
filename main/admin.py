from django.contrib import admin
from . import models

admin.site.register((
    models.ProductPhoto,
    models.Product,
    models.Characteristic,
    models.User,
    models.BrowsedProduct,
    models.Order,
    models.CartProduct,
    models.Feedback,
    models.Question,
), verbose_name_plural='Main')