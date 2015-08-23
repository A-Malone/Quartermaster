from scipy.optimize import basinhopping

from item_set_model import ItemSetModel

class SetOptimizer(object):
    """docstring for SetOptimizer"""

    minimizer_kwargs = {"method": "BFGS"}

    def __init__(self, model_name):
        super(SetOptimizer, self).__init__()
        self.model = ItemSetModel()
        self.model.load(model_name)

    input_array = np.zeros(somn_size)
    def objective_function(self, x):
        return self.model.predict(x)[0]

    def optimize(self, my_champ, other_champions, **kwargs):
        self.champion = my_champ
        self.other_champions = other_champions
        ret = basinhopping(func, x0, minimizer_kwargs=self.minimizer_kwargs,**kwargs)
