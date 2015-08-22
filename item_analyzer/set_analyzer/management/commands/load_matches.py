from django.core.management.base import BaseCommand
from set_analyzer.models import *
from set_analyzer.api_interface import *

import json

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _load_matches(self, w, filename):
        print("Loading matches from: '{}'".format(filename))

        with open(filename, 'r') as mfile:
            while(w.can_make_request()):
                match_id = int(mfile.readline())
                parse_match(w, w.get_match(match_id, include_timeline=True))

    def handle(self, *args, **options):
        w = RiotWatcher('7e6e61a1-243a-4739-a49d-78ec5a71ad71')
        #self._load_matches(w, args[0])

def parse_match(match_json):
    champ = Champion(champion_name='Veigar', champion_id=1)
    champ.save()
    print(champ)
