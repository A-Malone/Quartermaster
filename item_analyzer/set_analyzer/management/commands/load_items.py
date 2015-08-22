from django.core.management.base import BaseCommand
from set_analyzer.models import Item
from set_analyzer.api_interface import *

import json

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _load_items(self, w):
        Item.objects().all().delete()
        static_item_list = w.static_get_item_list()
        parse_items(static_item_list)

    def handle(self, *args, **options):
        w = RiotWatcher('7e6e61a1-243a-4739-a49d-78ec5a71ad71')
        self._load_items(w)

def parse_items(items):
    print(items)
