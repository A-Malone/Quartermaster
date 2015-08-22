from django.core.management.base import BaseCommand
from set_analyzer.models import Match
from set_analyzer.api_interface import *

import json, os, time

from django.conf import settings

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _load_matches(self, w, filename, start_index=0, num=10000):
        print("Loading matches from: '{}'".format(filename))

        i = 0

        abs_path = os.path.join(settings.BASE_DIR, 'item_analyzer', 'dataset', filename)

        with open(abs_path, 'r') as mfile:
            matches = json.load(mfile)

            if(start_index):
                matches[start_index:]

            for match_id in matches:
                print('Loading match: {}'.format(match_id))
                while(True):
                    if(w.can_make_request()):
                        if(i == num):
                            return
                        try:
                            match = Match.from_dict(w.get_match(match_id, include_timeline=True))
                            i+=1
                            break
                        except LoLException as le:
                            print("Too many requests, sleeping for 20s")
                            time.sleep(10)
                    else:
                        print("Too many requests, sleeping for 10s")

                    time.sleep(10)


    def handle(self, *args, **options):
        w = RiotWatcher('7e6e61a1-243a-4739-a49d-78ec5a71ad71')
        if(len(args)==1):
            self._load_matches(w, args[0])
        elif(len(args)==2):
            print('Loading {} matches'.format(args[1]))
            self._load_matches(w, args[0], num=int(args[1]))
        elif(len(args)==3):
            print('Loading {} matches starting at {}'.format(args[1], args[2]))
            self._load_matches(w, args[0], num=int(args[1]), start_index=int(args[2]))
        else:
            print('Bad args')
