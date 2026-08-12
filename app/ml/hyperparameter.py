import joblib

from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier


class HyperParameterOptimizer:

    def __init__(self):

        self.cv = StratifiedKFold(

            n_splits=5,

            shuffle=True,

            random_state=42

        )

    ############################################################

    def optimize_random_forest(
        self,
        X_train,
        y_train
    ):

        model = RandomForestClassifier(
            random_state=42,
            n_jobs=-1
        )

        params = {

            "n_estimators":[200,300,500],

            "max_depth":[10,15,20,None],

            "min_samples_split":[2,5,10],

            "min_samples_leaf":[1,2,4]

        }

        search = RandomizedSearchCV(

            estimator=model,

            param_distributions=params,

            n_iter=10,

            cv=self.cv,

            scoring="roc_auc",

            random_state=42,

            n_jobs=-1

        )

        search.fit(X_train,y_train)

        print("\nRandom Forest Best Parameters")

        print(search.best_params_)

        return search.best_estimator_

    ############################################################

    def optimize_xgboost(
        self,
        X_train,
        y_train
    ):

        model = XGBClassifier(

            random_state=42,

            eval_metric="logloss"

        )

        params = {

            "n_estimators":[200,300,500],

            "learning_rate":[0.01,0.05,0.1],

            "max_depth":[3,5,7],

            "subsample":[0.8,1.0],

            "colsample_bytree":[0.8,1.0]

        }

        search = RandomizedSearchCV(

            estimator=model,

            param_distributions=params,

            n_iter=10,

            cv=self.cv,

            scoring="roc_auc",

            random_state=42,

            n_jobs=-1

        )

        search.fit(X_train,y_train)

        print("\nXGBoost Best Parameters")

        print(search.best_params_)

        return search.best_estimator_

    ############################################################

    def optimize_lightgbm(
        self,
        X_train,
        y_train
    ):

        model = LGBMClassifier(
            random_state=42
        )

        params = {

            "n_estimators":[200,300,500],

            "learning_rate":[0.01,0.05,0.1],

            "num_leaves":[31,63,127],

            "max_depth":[5,10,-1]

        }

        search = RandomizedSearchCV(

            estimator=model,

            param_distributions=params,

            n_iter=10,

            cv=self.cv,

            scoring="roc_auc",

            random_state=42,

            n_jobs=-1

        )

        search.fit(X_train,y_train)

        print("\nLightGBM Best Parameters")

        print(search.best_params_)

        return search.best_estimator_

    ############################################################

    def optimize_catboost(
        self,
        X_train,
        y_train
    ):

        model = CatBoostClassifier(

            verbose=False,

            random_state=42

        )

        params = {

            "iterations":[200,300,500],

            "depth":[4,6,8],

            "learning_rate":[0.01,0.05,0.1]

        }

        search = RandomizedSearchCV(

            estimator=model,

            param_distributions=params,

            n_iter=10,

            cv=self.cv,

            scoring="roc_auc",

            random_state=42,

            n_jobs=-1

        )

        search.fit(X_train,y_train)

        print("\nCatBoost Best Parameters")

        print(search.best_params_)

        return search.best_estimator_

    ############################################################

    def save_model(
        self,
        model,
        filename
    ):

        joblib.dump(

            model,

            f"models/{filename}.joblib"

        )

        print(f"Saved {filename}")
