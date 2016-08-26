import os
import sys

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)


import config as config
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import cross_val_score

#
def build_model(df):
    """Build logistic regression model and run cross validation
    to check goodness of the model"""

    model = LogisticRegression()

    X = df[config.predictors]
    y = df["label"]

    model = model.fit(X, y)

    scores = cross_val_score(model, X, y, scoring='accuracy', cv=5)

    if scores.mean() < config.robust_model['mean'] or scores.std() > config.robust_model['std']:
        print "Model is broken. Call a data scientist."

    return model

