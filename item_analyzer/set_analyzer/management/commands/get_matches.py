from django.core.management.base import BaseCommand
from set_analyzer.models import Match
from set_analyzer.api_interface import *

import json, os, time, pickle

from django.conf import settings

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _load_matches(self, w, filename, start_index=0, num=10000):
        print("Loading matches from: '{}'".format(filename))

        i = 0

        abs_path = os.path.join(settings.BASE_DIR, 'item_analyzer', 'dataset', filename)
        cache_dir = os.path.join(settings.BASE_DIR, 'item_analyzer', 'dataset', 'cache')

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
                            match_dict = w.get_match(match_id, include_timeline=True)
                            match = Match.from_dict(match_dict)
                            with open(os.path.join(cache_dir, "{}.pkl".format(match_id)), 'wb') as f:
                                pickle.dump(match_dict, f)
                            i+=1
                            break
                        except LoLException as le:
                            print('League says: {}'.format(le.error))
                            print(le.headers)
                            time.sleep(2)
                    else:
                        print('Too many queries!')
                        pass

                time.sleep(1)


    def handle(self, *args, **options):
        api_path = os.path.join(settings.BASE_DIR, 'item_analyzer', 'APIkey.json')
        key = ''

        with open(api_path, 'r') as f:
            key = json.load(f)['key']

        print("Using API key: {}".format(key))

        w = RiotWatcher(key)
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
