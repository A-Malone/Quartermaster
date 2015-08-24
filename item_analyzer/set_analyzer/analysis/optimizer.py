from scipy.optimize import basinhopping
from set_analyzer.analysis.item_set_model import ItemSetModel
from set_analyzer.models import Champion, Item
import numpy as np

import random

class SetOptimizer(object):
    """docstring for SetOptimizer"""

    minimizer_kwargs = {"method": "BFGS"}
    stepsize = 20

    def __init__(self, model_name):
        super(SetOptimizer, self).__init__()
        self.model = ItemSetModel()
        self.model.load(model_name)
        self.item_ids = [x.item_id for x in Item.objects().all()]
        self.item_ids.sort()

    features = 25
    start_ind = 13
    input_array = np.zeros(25)
    def objective_function(self, x):
        self.input_array[self.start_ind:] = x
        return -self.model.predict(self.input_array)[0]

    class TakeStep(object):
        def __init__(self, items, stepsize=40):
            self.stepsize = stepsize
            self.item_ids = items
        def __call__(self, x):
            s = self.stepsize
            x_new = x.copy()
            for i in range(len(x)):
                curr = self.item_ids.index(x[i])
                start = max(0, round(curr - s/2))
                end = min(len(self.item_ids)-1, round(curr + s/2))
                x_new[i] = self.item_ids[random.randint(start, end)]

            return x_new

    def optimize(self, cid, other_champion_stats):
        champion = Champion.objects(champion_id=cid).get()
        self.input_array[0] = cid
        self.input_array[1:7] = np.array(champion.class_data)
        self.input_array[7:self.start_ind] = np.array(other_champion_stats)
        x0 = [random.choice(self.item_ids) for x in range(12)]

        ret = basinhopping(
            self.objective_function,
            x0,
            take_step=self.TakeStep(self.item_ids, self.stepsize),
            minimizer_kwargs=self.minimizer_kwargs,
            niter=100,
            stepsize=100,
            T=10.0
        )
        return ret
