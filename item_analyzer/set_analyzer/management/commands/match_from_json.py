from django.core.management.base import BaseCommand
from set_analyzer.models import Match
from set_analyzer.api_interface import *

import json, os

from django.conf import settings

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _load_match(self, filename):
        print("Loading match from: '{}'".format(filename))
        abs_path = os.path.join(settings.BASE_DIR, 'item_analyzer', 'dataset', filename)
        with open(abs_path, 'r') as mfile:
            match_data = json.load(mfile)
            match = Match.from_dict(match_data)
            match.save()


    def handle(self, *args, **options):
        if(len(args)==1):
            self._load_match(args[0])
        else:
            print('Bad args')
