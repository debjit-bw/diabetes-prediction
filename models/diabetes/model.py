import pickle
import pandas as pd
from sklearn import preprocessing

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import GridSearchCV

class model:
    def __init__(self, retrain = False) -> None:
        
        if retrain == True:
            df = pd.read_csv("./models/diabetes/data.csv")

            label_encoder = preprocessing.LabelEncoder()

            for column in df.columns[1:]:
                df[column] = label_encoder.fit_transform(df[column])

            x_train = df.drop(['class'], axis= 1)
            y_train = df['class']


            clf1 = RandomForestClassifier(random_state=1)
            clf2 = GradientBoostingClassifier(random_state=1)
            clf3 =  DecisionTreeClassifier(random_state=1)

            params={"rf__max_depth":[8],
                    "rf__criterion":["entropy"],
                    "rf__n_estimators":[1000],
                    "gb__loss":["deviance"],
                    "gb__n_estimators":[1000],
                    "gb__criterion":["friedman_mse"],
                    "gb__max_depth":[2],
                    "gb__max_features":["auto"],
                    "dt__max_features":["auto"],
                    "dt__criterion":["gini"],
                    "dt__max_depth":[16]
                    }

            eclf = VotingClassifier(estimators=[("rf", clf1), ("gb", clf2), ("dt", clf3)],
                                voting= 'soft', weights = [3,1,1])
            grid = GridSearchCV(estimator=eclf, param_grid=params, cv=5)
            grid.fit(x_train, y_train)
            pickle.dump(grid, open("./models/diabetes/model.obj", mode = "wb"))
        
        else:
            grid = pickle.load(open("./models/diabetes/model.obj", mode = "rb"))

        self.out = grid.best_estimator_.predict_proba

    def predict(self, inputs):
        return self.out([inputs])[0]

    