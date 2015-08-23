from django.core.management.base import BaseCommand
from set_analyzer.analysis.item_set_model import ItemSetModel

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _generate_model(self, filename):
        print("Generating model...")
        model = ItemSetModel()
        model.train(train_ratio=0.8)
        print("Saving model to file...")
        model.save(filename)

    def handle(self, *args, **options):
        if(len(args)==1):
            self._generate_model(args[0])
        else:
            print('Bad args')
