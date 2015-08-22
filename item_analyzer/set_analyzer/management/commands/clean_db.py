from django.core.management.base import BaseCommand
from set_analyzer.models import *
from set_analyzer.api_interface import *
from functools import reduce
import sys

import json

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _clean_db(self, user_list=None):
        str_to_cls = lambda  x : reduce(getattr, x.split("."), sys.modules[__name__])
        if(user_list):
            to_clean = [str_to_cls(x) for x in user_list]
        else:
            to_clean = [Champion, Item, Match]
        for cls in to_clean:
            print("Deleting all records for class: {}".format(cls.__name__))
            cls.objects().all().delete()

    def handle(self, *args, **options):
        self._clean_db(args)
