from django.core.management.base import BaseCommand
from set_analyzer.models import Item
from set_analyzer.api_interface import *

from django.conf import settings

import json, os

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _load_items(self, w):
        versions = ["5.11.1", "5.14.1"]
        for version in versions:
            static_item_list = w.static_get_item_list(item_list_data='gold,stats,into,from', version=version)
            for item_id, item_dict in static_item_list['data'].items():
                item_dict['version'] = version
                item = Item.from_dict(item_dict)
                item.save()

    def handle(self, *args, **options):
        api_path = os.path.join(settings.BASE_DIR, 'item_analyzer', 'APIkey.json')
        key = ''

        with open(api_path, 'r') as f:
            key = json.load(f)['key']

        w = RiotWatcher(key)
        self._load_items(w)

def parse_items(items):
    print(items)
