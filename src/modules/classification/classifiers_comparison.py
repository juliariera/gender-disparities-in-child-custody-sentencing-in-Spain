import numpy as np

from sklearn.metrics import balanced_accuracy_score

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier

from sklearn.model_selection import StratifiedKFold


def model_comparison(df, target_var, hide_cols):
    
    # Prepare the data
    cols = [i for i in df.columns if i not in (target_var)]
    cols = [i for i in cols if i not in (hide_cols)]
    X = df[cols].to_numpy()
    y = df[target_var].to_numpy()    

    # Define the classifiers to compare
    clf_names = ["LogReg", "RandomForest", "SVM linear", "SVM RBF kernel", "AdaBoost"]
    clfs = [LogisticRegression(random_state=0, C=1, max_iter=1000, solver='lbfgs'), RandomForestClassifier(n_estimators = 1000), SVC(gamma='auto', kernel='linear'), SVC(gamma='auto', kernel='rbf'), AdaBoostClassifier(n_estimators=1000, random_state=0)]

    # Create a cross validator with 5 splits
    cv = StratifiedKFold(n_splits=5)
    cv.get_n_splits(X, y)

    model_performances = {}

    #For each partition
    for train_index, test_index in cv.split(X, y):

        for clf, clf_name in zip(clfs, clf_names):

            _X_train, _X_test = X[train_index], X[test_index]
            _y_train, _y_test = y[train_index], y[test_index]

            # Model training
            clf.fit(_X_train, _y_train) 

            # Model testing
            y_pred = clf.predict(_X_test)

            # Performance: balanced accuracy metric
            perf = balanced_accuracy_score(_y_test, y_pred)

            if clf_name not in model_performances:
                model_performances[clf_name] = []
            # Store performance in the dict    
            model_performances[clf_name].append(perf) 

    # Print average performance per model
    for clf_name in clf_names:
        print("%s - %.3f" % (clf_name, np.mean(model_performances[clf_name])))
        
        
