from django.core.management.base import BaseCommand
from set_analyzer.models import *

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _load_matches(self, filename):
        print("Loading matches from: '{}'".format(filename))
        champ = Champion(champion_name='Veigar', champion_id=1)
        champ.save()
        print(champ)

    def handle(self, *args, **options):
        self._load_matches(args[0])
