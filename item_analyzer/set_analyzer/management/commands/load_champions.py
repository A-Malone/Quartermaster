from django.core.management.base import BaseCommand
from set_analyzer.models import Champion
from set_analyzer.api_interface import *

import json

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _load_champions(self, w):
        static_champ_list = w.static_get_champion_list()
        for cname in static_champ_list['data']:
            champion = Champion.from_dict(static_champ_list['data'][cname])
            champion.save()

    def handle(self, *args, **options):
        w = RiotWatcher('7e6e61a1-243a-4739-a49d-78ec5a71ad71')
        self._load_champions(w)
