from django.core.management.base import BaseCommand
from set_analyzer.models import Champion
from set_analyzer.api_interface import *

from django.conf import settings

import json, os

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _load_champions(self, w):
        static_champ_list = w.static_get_champion_list(champ_data='tags')
        for cname in static_champ_list['data']:
            champion = Champion.from_dict(static_champ_list['data'][cname])
            champion.save()

    def handle(self, *args, **options):
        api_path = os.path.join(settings.BASE_DIR, 'item_analyzer', 'APIkey.json')
        key = ''

        with open(api_path, 'r') as f:
            key = json.load(f)['key']

        w = RiotWatcher(key)
        self._load_champions(w)
