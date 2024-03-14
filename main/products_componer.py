from typing import Union, Dict, Tuple, List, Any, Iterable
from abc import ABC, abstractmethod
from functools import lru_cache
from django.db.models.query import QuerySet
from django.db.models import Q
from functools import reduce
from math import ceil
from .tools import get, get_related_models
from .models import Characteristic, Product
from . import field_choices as choices
from .translations import CHARACTERISTIC_CATEGORIES, CHARACTERISTIC_FIELDS, CHARACTERISTIC_CHOICES, CHARACTERISTIC_ENDINGS

class BaseFilters(ABC):
    @abstractmethod
    def get_filters_data(self, lang:str) -> Dict[str, Union[str, List[Dict[str,str]] ]]:
        '''
        Returns all need data for view.
        
        `data: { field:str, field_label:str, filters: List({ key:str, label:str }) }`
        '''
        pass

    @abstractmethod
    def get_Q(self, keys:List[str]) -> Union[Q, Tuple[Q]]:
        'Returns Q parameter/parameters for filtering characteristic'
        pass

    def __init__(self, field:str):
        self.field = field
        self.field_label = CHARACTERISTIC_FIELDS[field]

class Range():
    def __init__(self, lower:Union[int,float,None], upper:Union[int,float,None]):
        if lower is None and upper is None:
            raise Exception('All bounds is None')
        
        self.lower = lower
        self.upper = upper

class FilterRanges(BaseFilters):
    ranges:Dict[str,Any]
    params:Dict[str,str]

    __lte_labels = {
        'ua': '{} і менше',
        'en': 'Less or equal to {}',
    }
    __gte_labels = {
        'ua': '{} і більше',
        'en': 'Greater or equal to {}',
    }

    @lru_cache(maxsize=None)
    def get_filters_data(self, lang:str) -> Dict[str, Union[str, List[Dict[str,str]] ]]:
        data = {
            'field': self.field,
            'field_label': self.field_label[lang],
            'filters': [],
        }

        if self.endings is None or isinstance(self.endings, str):
            ending = self.endings
        else:
            ending = self.endings[lang]

        lte_labels, gte_labels = FilterRanges.__lte_labels, FilterRanges.__gte_labels
        
        
        for key, rng in self.ranges.items():

            if rng.lower == None:
                label = lte_labels[lang].format(f'{rng.upper}{ending}')

            elif rng.upper == None:
                label = gte_labels[lang].format(f'{rng.lower}{ending}')

            else:
                label = f'{rng.lower}{ending} - {rng.upper}{ending}'

            data['filters'].append({
                'key': key,
                'label': label,
            })

        return data

    def get_Q(self, keys:List[str]) -> Tuple[Q]:
        return tuple(Q(**self.params[key]) for key in self.params.keys() if key in keys)

    def __set_ranges_params__(self, ranges:Tuple[Range]):
        self.ranges = {}
        self.params = {}

        for rng in ranges:

            if rng.lower == None:
                key = f'lte_{rng.upper}'
                param = {f'{self.field}__lte': rng.upper}
            
            elif rng.upper == None:
                key = f'gte_{rng.lower}'
                param = {f'{self.field}__gte': rng.lower}

            else:
                key = f'{rng.lower}-{rng.upper}'
                param = {f'{self.field}__range': (rng.lower, rng.upper)}
            
            self.ranges[key] = rng
            self.params[key] = param

    def __init__(self, *ranges:Range, field:str, endings:Union[str, Dict[str, str]]=None):
        super().__init__(field)
        self.endings = endings
        self.__set_ranges_params__(ranges)

class FilterChoices(BaseFilters):
    __labels:Dict[str, Union[str, Dict[str,str]]]
    LABELS_OTHER = {'other': {'ua': 'Інше', 'en': 'Other'}}
    
    def get_filters_data(self, lang:str) -> Dict[str, Union[str, List[Dict[str,str]] ]]:
        data = {
            'field': self.field,
            'field_label': self.field_label[lang],
            'filters': [],
        }

        for key in self.keys:
            label = self.__labels[key]
            data['filters'].append({
                'key': key,
                'label': label if isinstance(label, str) else label[lang],
            })
        
        return data

    def get_Q(self, keys:List[str]) -> Q:
        valid_keys = tuple(key for key in self.keys if str(key) in keys)
        return Q(**{f'{self.field}__in': valid_keys})

    def __init__(self, field:str, choices:Tuple[Tuple[Any, str]], labels:Dict[str, Union[str, Dict[str,str]]]={}):
        super().__init__(field)
        self.keys = set()
        self.__labels = {}

        for choice in choices:
            key = choice[0]
            self.keys.add(key)
            self.__labels[key] = labels[key] if key in labels else choice[1]

__filters_data:Dict[str,BaseFilters] = {
    'manufacturer': FilterChoices(
        field='manufacturer',
        choices=choices.MANUFACTURERS,
        labels=FilterChoices.LABELS_OTHER
    ),
    'os': FilterChoices(
        field='os',
        choices=choices.OPERATING_SYSTEMS,
        labels=FilterChoices.LABELS_OTHER
    ),
    'diagonal': FilterRanges(
        Range(None, 4.59),
        Range(4.6,  4.99),
        Range(5.0,  5.49),
        Range(5.5,  5.99),
        Range(6.0,  6.5),
        Range(6.51, None),
        field='diagonal',
        endings='"'
    ),
    'matrix': FilterChoices(
        field='matrix',
        choices=choices.MATRICES,
        labels=FilterChoices.LABELS_OTHER
    ),
    'screen_frequency': FilterRanges(
        Range(None, 59),
        Range(60,   89),
        Range(90,   119),
        Range(120,  143),
        Range(144,  165),
        Range(166,  None),
        field='screen_frequency',
        endings=CHARACTERISTIC_ENDINGS['GHz']
    ),
    'connection_types': FilterChoices(
        field='connection_types',
        choices=choices.CONNECTION_TYPES
    ),
    'sim_number': FilterChoices(
        field='sim_number',
        choices=choices.SIM_NUMBERS
    ),
    'sim_size': FilterChoices(
        field='sim_size',
        choices=choices.SIM_SIZES,
        labels=FilterChoices.LABELS_OTHER
    ),
    'ram': FilterRanges(
        Range(None, 2),
        Range(3,    6),
        Range(8,    18),
        Range(32,   None),
        field='ram',
        endings=CHARACTERISTIC_ENDINGS['Gb']
    ),
    'rom': FilterRanges(
        Range(None, 16),
        Range(32,   128),
        Range(256,  512),
        Range(1024, None),
        field='rom',
        endings=CHARACTERISTIC_ENDINGS['Gb']
    ),
    'max_size_additional_memory': FilterRanges(
        Range(None, 16),
        Range(32,   128),
        Range(256,  512),
        Range(1024, None),
        field='max_size_additional_memory',
        endings=CHARACTERISTIC_ENDINGS['Gb']
    ),
    'main_camera': FilterRanges(
        Range(None, 5),
        Range(6,    8.9),
        Range(9,    14),
        Range(15,   19),
        Range(20,   48),
        Range(49,   64),
        Range(65,   99),
        Range(100, None),
        field='main_camera',
        endings=CHARACTERISTIC_ENDINGS['Mp']
    ),
    'number_main_cameras': FilterChoices(
        field='number_main_cameras',
        choices=choices.NUMBER_OF_CAMERAS
    ),
    'main_camera_features': FilterChoices(
        field='main_camera_features',
        choices=choices.MAIN_CAMERA_FEATURES,
        labels=CHARACTERISTIC_CHOICES['main_camera_features']
    ),
    'front_camera': FilterRanges(
        Range(None, 5),
        Range(6,    8.9),
        Range(9,    16),
        Range(17,   20),
        Range(21,   30),
        Range(31,   39),
        Range(40, None),
        field='front_camera',
        endings=CHARACTERISTIC_ENDINGS['Mp']
    ),
    'battery_volume': FilterRanges(
        Range(None, 2999),
        Range(3000, 3999),
        Range(4000, 4999),
        Range(5000, 6000),
        Range(6001, None),
        field='battery_volume',
        endings=CHARACTERISTIC_ENDINGS['mAh']
    ),
    'wirelesses': FilterChoices(
        field='wirelesses',
        choices=choices.WIRELESSES,
        labels=CHARACTERISTIC_CHOICES['wirelesses']
    ),
    'connectors': FilterChoices(
        field='connectors',
        choices=choices.CONNECTORS
    ),
    'security': FilterChoices(
        field='security',
        choices=choices.SECURITY,
        labels=CHARACTERISTIC_CHOICES['security']
    ),
    'features': FilterChoices(
        field='features',
        choices=choices.FEATURES,
        labels=CHARACTERISTIC_CHOICES['features']
    ),
}

def get_characteristic_for_view(characteristic:Characteristic, lang:str) -> Dict[str, Dict[str, Union[str,None]]]:
    get_category  = lambda name: CHARACTERISTIC_CATEGORIES[name][lang]
    get_chr       = lambda name: CHARACTERISTIC_FIELDS[name][lang]
    get_ending    = lambda name: CHARACTERISTIC_ENDINGS[name][lang]
    get_textfield = lambda **fields: fields[lang].replace(';;', '<br>') if fields[lang] else None

    def get_choices(keys:Iterable, data:Union[Tuple, Dict]):
        labels = []

        if isinstance(data, tuple):
            for key in keys:
                for choice in data:
                    if key == choice[0]:
                        labels.append(choice[1])
        else:
            for key in keys:
                labels.append(data[key][lang])
        
        return '<br>'.join(labels)

    def get_choice(key:str, data:Union[Tuple, Dict]):
        if isinstance(data, tuple):
            if key == 'other':
                return 'Інше' if lang == 'ua' else 'Other'

            for choice in data:
                if key == choice[0]:
                    return choice[1]

        return data[key][lang]

    ch = characteristic

    return {
        get_category('main'): {
            get_chr('manufacturer'): get_choice(ch.manufacturer, choices.MANUFACTURERS),
            get_chr('os'):           get_choice(ch.os, choices.OPERATING_SYSTEMS),
        },
        get_category('display'): {
            get_chr('diagonal'):         f'{ch.diagonal}"',
            get_chr('resolution'):       f'{ch.horizontal_resolution}x{characteristic.vertical_resolution}',
            get_chr('matrix'):           get_choice(ch.matrix, choices.MATRICES),
            get_chr('screen_frequency'): f'{ch.screen_frequency}{get_ending("GHz")}',
            get_chr('screen_material'):  ch.screen_material,
        },
        get_category('connecting'): {
            get_chr('connection_types'): get_choices(ch.connection_types, choices.CONNECTION_TYPES),
            get_chr('sim_number'):       get_choice(ch.sim_number, choices.SIM_NUMBERS),
            get_chr('sim_size'):         get_choice(ch.sim_size, choices.SIM_SIZES),
        },
        get_category('memory'): {
            get_chr('ram'):               f'{ch.ram}{get_ending("Gb")}',
            get_chr('rom'):               f'{ch.rom}{get_ending("Gb")}',
            get_chr('additional_memory'): ch.additional_memory,
            get_chr('max_size_additional_memory'): f'{ch.max_size_additional_memory}{get_ending("Gb")}',
        },
        get_category('main_camera'): {
            get_chr('main_camera'):           f'{ch.main_camera}{get_ending("Mp")}',
            get_chr('number_main_cameras'):   get_choice(ch.number_main_cameras, choices.NUMBER_OF_CAMERAS),
            get_chr('main_camera_features'):  get_choices(ch.main_camera_features, CHARACTERISTIC_CHOICES['main_camera_features']),
            get_chr('main_camera_video'):     ch.main_camera_video,
            get_chr('main_camera_additions'): get_textfield(ua=ch.main_camera_additions_ua, en=ch.main_camera_additions_en),
        },
        get_category('front_camera'): {
            get_chr('front_camera'):           f'{ch.front_camera}{get_ending("Mp")}',
            get_chr('front_camera_video'):     ch.front_camera_video,
            get_chr('front_camera_additions'): get_textfield(ua=ch.front_camera_additions_ua, en=ch.front_camera_additions_en),
        },
        get_category('processor'): {
            get_chr('processor'):           ch.processor,
            get_chr('videocore'):           ch.videocore,
            get_chr('number_cores'):        str(ch.number_cores),
            get_chr('processor_frequency'): f'{ch.processor_frequency}{get_ending("GHz")}',
        },
        get_category('dimensions'): {
            get_chr('weight'): f'{ch.weight}{get_ending("g")}',
            get_chr('width'):  f'{ch.width}{get_ending("mm")}',
            get_chr('height'): f'{ch.height}{get_ending("mm")}',
            get_chr('depth'):  f'{ch.depth}{get_ending("mm")}',
        },
        get_category('addition'): {
            get_chr('battery_volume'): f'{ch.battery_volume}{get_ending("mAh")}',
            get_chr('wirelesses'):     get_choices(ch.wirelesses, CHARACTERISTIC_CHOICES['wirelesses']),
            get_chr('connectors'):     get_choices(ch.connectors, choices.CONNECTORS),
            get_chr('security'):       get_choices(ch.security, CHARACTERISTIC_CHOICES['security']),
            get_chr('protection'):     ch.protection,
            get_chr('sensors'):        get_textfield(ua=ch.sensors_ua, en=ch.sensors_en),
            get_chr('features'):       get_choices(ch.features, CHARACTERISTIC_CHOICES['features']),
            get_chr('additions'):      get_textfield(ua=ch.additions_ua, en=ch.additions_en),
        },
    }

def get_filters_for_view(lang:str):
    filters_map = ({
            'category': 'main',
            'fields':   ('manufacturer', 'os'),
        }, {
            'category': 'display',
            'fields':   ('diagonal', 'matrix', 'screen_frequency'),
        }, {
            'category': 'connecting',
            'fields':   ('connection_types', 'sim_number', 'sim_size'),
        }, {
            'category': 'memory',
            'fields':   ('ram', 'rom', 'max_size_additional_memory'),
        }, {
            'category': 'cameras',
            'fields':   ('main_camera', 'number_main_cameras', 'main_camera_features', 'front_camera'),
        }, {
            'category': 'addition',
            'fields':   ('battery_volume', 'wirelesses', 'connectors', 'security', 'features'),
        },
    )
    
    data = {}

    for item in filters_map:
        category = CHARACTERISTIC_CATEGORIES[item['category']][lang]
        filters = tuple(__filters_data[field].get_filters_data(lang) for field in item['fields'])
        data[category] = filters

    return data

def get_filtered_characteristics(filter_data:Dict[str,str]) -> QuerySet[Characteristic]:
    characteristics = Characteristic.objects.all()

    if not filter_data:
        return characteristics

    filters = __filters_data
    Qs = []

    for field in filters.keys():
        if field in filter_data:

            keys = filter_data[field].split(',')
            q = filters[field].get_Q(keys)

            Qs.append(q) if isinstance(q, Q) else Qs.extend(q)
    
    if not Qs:
        return characteristics
    
    return characteristics.filter(reduce(lambda x, y: x | y, Qs))

def get_filtered_and_sort_products(data:Dict[str,str]) -> QuerySet[Product]:
    # Filter products
    characteristics = get_filtered_characteristics(data)
    products = get_related_models(characteristics, Product, 'product')
    
    if 'src' in data:
        products = products.filter(name__icontains=data['src'])

    if 'discount' in data:
        products = products.filter(discount__gt=0)

    # Sort products
    sort = get(data, key='sort', default='rating')
    
    if sort == 'price_c2e':
        products = products.order_by('price')
    
    elif sort == 'price_e2c':
        products = products.order_by('-price')

    elif sort == 'date':
        products = products.order_by('-date_of_issue')
    
    else:
        products = products.order_by('-avr_rating')
    
    return products

def get_activePage_allPages_productsFromPage(products:QuerySet[Product], data:Dict[str,str], products_on_page=40) -> Tuple[int, int, QuerySet[Product]]:
    # all pages
    products_count = products.count()

    if products_count <= products_on_page:
        return (1, 1, products)

    all_pages = ceil(products_count / products_on_page)

    # active page
    page = get(data, key='page', default='1')
    page = int(page) if page.isdigit() else 1

    if page < 1:
        page = 1
    elif page > all_pages:
        page = all_pages
    
    #products
    start = (page - 1) * products_on_page
    products_from_page = products[start : start + products_on_page]

    return (page, all_pages, products_from_page)