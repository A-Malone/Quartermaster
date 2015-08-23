from django.core.management.base import BaseCommand
from set_analyzer.analysis.item_set_model import ItemSetModel

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _generate_model(self, filename, cached=False):
        print("Generating model...")
        model = ItemSetModel()
        if(not cached):
            print("Assembling data...")
            X, Y = model.get_data_sets(cache=True)
        else:
            print("Loading cached data...")
            X, Y = model.get_cached_data()

        model.train(X, Y, train_ratio=0.8)
        print("Saving model to file...")
        model.save(filename)

    def handle(self, *args, **options):
        if(len(args)==1):
            self._generate_model(args[0])
        elif(len(args)==2 and args[1] == 'cached'):
            self._generate_model(args[0], cached=True)
        else:
            print('Bad args')
