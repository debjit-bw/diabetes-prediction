import pickle
import numpy as np
import pandas as pd
from sklearn import preprocessing

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import GridSearchCV


class model:
    def __init__(self, retrain=False, use_legacy=False) -> None:

        if use_legacy == True:
            self.using_legacy = True

            if retrain == True:
                df = pd.read_csv("./models/diabetes/data.csv")

                label_encoder = preprocessing.LabelEncoder()

                for column in df.columns[1:]:
                    df[column] = label_encoder.fit_transform(df[column])

                x_train = df.drop(["class"], axis=1)
                y_train = df["class"]

                clf1 = RandomForestClassifier(random_state=1)
                clf2 = GradientBoostingClassifier(random_state=1)
                clf3 = DecisionTreeClassifier(random_state=1)

                params = {
                    "rf__max_depth": [8],
                    "rf__criterion": ["entropy"],
                    "rf__n_estimators": [1000],
                    "gb__loss": ["deviance"],
                    "gb__n_estimators": [1000],
                    "gb__criterion": ["friedman_mse"],
                    "gb__max_depth": [2],
                    "gb__max_features": ["auto"],
                    "dt__max_features": ["auto"],
                    "dt__criterion": ["gini"],
                    "dt__max_depth": [16],
                }

                eclf = VotingClassifier(
                    estimators=[("rf", clf1), ("gb", clf2), ("dt", clf3)],
                    voting="soft",
                    weights=[3, 1, 1],
                )
                grid = GridSearchCV(estimator=eclf, param_grid=params, cv=5)
                grid.fit(x_train, y_train)
                pickle.dump(grid, open("./models/diabetes/model.obj", mode="wb"))

            else:
                grid = pickle.load(open("./models/diabetes/model.obj", mode="rb"))

            self.out = grid.best_estimator_

        else:
            self.using_legacy = False

            if retrain == True:
                df = pd.read_csv("./models/diabetes/data.csv")
                label_encoder = preprocessing.LabelEncoder()
                for column in df.columns[1:]:
                    df[column] = label_encoder.fit_transform(df[column])

                self.importance = np.array(np.abs(df.iloc[:,:-1].corrwith(df['class'])))
                self.importance /= self.importance.sum()

                np.save("./models/diabetes/model.npy", self.importance)
            else:
                self.importance = np.load("./models/diabetes/model.npy")

    def predict(self, inputs):
        if self.using_legacy == True:
            result = self.out.predict_proba([inputs])[0][1]
            result = int((result - 0.3)/(1.0 - 0.3)*100)
            if result < 0:
                return 0
            else:
                return result
        else:
            inputs = np.array(inputs)
            if inputs[0] > 0 and inputs[0] < 100:
                inputs[0] /= 100
            else:
                inputs[0] = 0

            result = np.dot(self.importance, inputs) * 100

            return int(result)

    def predictp(self, inputs):
        return self.out.predict([inputs])
