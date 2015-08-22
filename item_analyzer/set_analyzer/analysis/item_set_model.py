import sklearn
from sklearn import tree
from sklearn import cross_validation, preprocessing
from sklearn.metrics import classification_report, r2_score
from sklearn.externals import joblib

from set_analyzer.models import *

import numpy as np

from django.conf import settings

#IDEA
#Machine learning model to make the data smooth and continuous
#   -> sklearn
#Simulated annealing or other similar algorithm to solve for the local maximum
#   -> scipy.optimize.basinhopping

class ItemSetModel(object):
    """docstring for ItemSetModel"""

    clf = None

    MODEL_PATH = os.path.join(settings.BASE_DIR, 'setanalyzer', 'analysis', 'models')

    def __init__(self):
        super(ItemSetModel, self).__init__()
        self.clf = tree.DecisionTreeRegressor()

    def get_data_sets(self, **kwargs):
        """
        Data Schema:
            Input:
                My champion ID
                [Other team's champion ID's]
                [7 Final Items]
                [first 5 items purchased]
                ________________________________________
                18 features

            Output:
                Score = A(Gold/time) + B(xp/time) + C(win)
                ________________________________________
                1 Output

        """
        matches = Match.objects.all(**kwargs)

        #Presize data
        features = 18
        outputs = 1
        num_participants = len(matches)*10
        input_data = np.zeros((num_participants, features))
        output_data = np.zeros((num_participants, outputs))

        for match in matches:
            pass

    def train(self, **kwargs):
        X = None
        Y = None
        self.clf.fit(X,Y)

    def predict(self, X):
        return self.clf.predict(X)

    #LOAD AND SAVE
    def save(self, filename):
        path = os.path.join(self.MODEL_PATH, filename)
        joblib.dump(self.clf, path)

    def load(self, filename):
        path = os.path.join(self.MODEL_PATH, filename)
        self.clf = joblib.load(path)


#MODEL EVAUATION
def k_fold_evaluate(clf, X, y, folds):
    print("Running K-Folding: {} folds on {} rows".format(folds, len(X)))
    this_scores = cross_validation.cross_val_score(self.model, X, y, n_jobs=-1, cv=folds)
    print("k_folding results: {}\n".format(this_scores))

def get_classification_report(clf, X, y):
    results_array = np.zeros((len(self.classifiers), len(X)))
    predicted_data = clf.predict(X)
    R2 = clf.score(X, y)
    print("Model R squared: {} -- {}\n".format(R2,type(clf)))
    report = classification_report(y, predicted_data, target_names=self.get_bucket_names())
    print(report)

def chi_squared(m, y, v):
    """My own R^2 check"""
    y_var = np.var(y)
    t = 0
    for i in range(v):
        t += (y[i] - m[i])**2
    return 1 - t / y_var / v
