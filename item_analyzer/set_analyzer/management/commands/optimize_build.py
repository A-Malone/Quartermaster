from django.core.management.base import BaseCommand
from set_analyzer.models import Item
from set_analyzer.api_interface import *

from set_analyzer.analysis.optimizer import SetOptimizer

from django.conf import settings

import json, os

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _optimize_build(self):
        opt = SetOptimizer('RandomForest_updated')
        res = opt.optimize(72, [4,1,1,1,1,1])
        for item in res.x:
            print(Item.objects(item_id=item).first().name)

    def handle(self, *args, **options):
        self._optimize_build()
