from typing import Dict
from django.db.models import QuerySet, Model

def get(dictionary:Dict, key, default):
    '''
    Returns value from `dictionary` for the `key` if the `key` is found in `dictionary`
    or return `default` if the `key` not found or value is None
    '''
    value = dictionary.get(key, default)
    return value if value else default

def get_related_models(models:QuerySet, related_type:Model, related_name:str) -> QuerySet:
    'Returns all related models of type `related_type` from `models` from field with name `related_name`'
    ids = models.values_list(related_name, flat=True)
    return related_type.objects.filter(id__in=ids)