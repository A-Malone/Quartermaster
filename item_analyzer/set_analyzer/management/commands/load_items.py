from django.core.management.base import BaseCommand
from set_analyzer.models import Item
from set_analyzer.api_interface import *

import json

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _load_items(self, w):
        versions = ["5.11.1", "5.14.1"]
        for version in versions:
            static_item_list_gold = w.static_get_item_list(item_list_data='gold', version=version)
            static_item_list_stats = w.static_get_item_list(item_list_data='stats', version=version)
            for item_id, item_dict in static_item_list_gold['data'].items():
                item_dict.update(static_item_list_stats['data'][item_id])
                item_dict['version'] = version 
                item = Item.from_dict(item_dict)
                item.save()

    def handle(self, *args, **options):
        w = RiotWatcher('7e6e61a1-243a-4739-a49d-78ec5a71ad71')
        self._load_items(w)

def parse_items(items):
    print(items)
