from django.core.management.base import BaseCommand
from set_analyzer.models import Match
from set_analyzer.api_interface import *

import json

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _load_matches(self, w, filename, num=1):
        print("Loading matches from: '{}'".format(filename))

        i = 0

        with open(filename, 'r') as mfile:
            while(w.can_make_request() and i<num):
                match_id = int(mfile.readline())
                match = Match.from_dict(w.get_match(match_id, include_timeline=True))
                match.save()
                i+=1

    def handle(self, *args, **options):
        w = RiotWatcher('7e6e61a1-243a-4739-a49d-78ec5a71ad71')
        if(len(args)==1):
            self._load_matches(w, args[0])
        elif(len(args)==2):
            self._load_matches(w, args[0], args[1])
        else:
            print('Bad args')
