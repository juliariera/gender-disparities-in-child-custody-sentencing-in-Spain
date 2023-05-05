import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import StratifiedKFold

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier

from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import confusion_matrix


def lr_classifier(df, target_var, hide_cols, printInfo = True):
    clf = LogisticRegression(random_state=0, C=1, max_iter=1000, solver='lbfgs')
    return classifier(clf, df, target_var, hide_cols, printInfo, log_reg = True)

def ab_classifier(df, target_var, hide_cols, printInfo = True):
    clf = AdaBoostClassifier(n_estimators=1000, random_state=0)
    return classifier(clf, df, target_var, hide_cols, printInfo)

def rf_classifier(df, target_var, hide_cols, printInfo = True):
    clf = RandomForestClassifier(n_estimators = 1000)
    return classifier(clf, df, target_var, hide_cols, printInfo)


def classifier(clf, df, target_var, hide_cols, printInfo, log_reg = False):
    
    # Prepare the data
    cols = [i for i in df.columns if i not in (target_var)]
    cols = [i for i in cols if i not in (hide_cols)]
    X = df[cols].to_numpy()
    y = df[target_var].to_numpy()

    # Create a cross validator with 5 splits
    cv = StratifiedKFold(n_splits=5)
    cv.get_n_splits(X, y)

    balanced_accuracy_list = []
    feature_importances_list = []
    confusion_matrices = dict.fromkeys(["tn", "fp", "fn", "tp"])
    for key in confusion_matrices.keys():
        confusion_matrices[key] = []
    
    #For each partition
    for train_index, test_index in cv.split(X, y):

        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        # Model training
        clf.fit(X_train, y_train) 

        # Model testing
        y_pred = clf.predict(X_test)
        y_prob = clf.predict_proba(X_test)


        # Performance: balanced accuracy
        balanced_accuracy = balanced_accuracy_score(y_test, y_pred) 
        balanced_accuracy_list.append(balanced_accuracy)

        # Feature importances
        if(log_reg == False):
            feture_importances = clf.feature_importances_
        else:
            feture_importances = clf.coef_.ravel()
        feature_importances_list.append(feture_importances)

        # Confussion matrix values
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()            
        confusion_matrices["tn"].append(tn)
        confusion_matrices["fp"].append(fp)
        confusion_matrices["fn"].append(fn)
        confusion_matrices["tp"].append(tp)

            
    # Performance: mean
    if(printInfo):
        print("Balanced accuracy mean: " + str(np.mean(balanced_accuracy_list)))
    
    # Feature importances: median
    feature_importances_stack = np.stack(feature_importances_list, axis=0)
    median_feature_importances = np.median(feature_importances_stack, axis = 0)
    
    coefficients = pd.DataFrame(median_feature_importances)
    features = pd.DataFrame(cols)
    feature_coefficients = (pd.merge(features, coefficients,left_index= True, right_index= True, how = "left"))
    #feature_coefficients.columns = ["features", "coefficients"]
    
    # Feature importances: std
    std_feature_importances = np.std(feature_importances_stack, axis = 0)
    std = pd.DataFrame(std_feature_importances)
    feature_coefficients = (pd.merge(feature_coefficients,std,left_index= True, right_index= True, how = "left"))
    feature_coefficients.columns = ["features", "coefficients", "std"]

    # Confusion matrix: mean
    
    # create
    confusion_matrix_means = []
    for value in confusion_matrices.keys():
        confusion_matrix_means.append(np.mean(confusion_matrices[value]))
        
    # display
    if(printInfo):
        confusion_matrix_means_2d_array = np.array([[confusion_matrix_means[0], confusion_matrix_means[1]],
                                           [confusion_matrix_means[2], confusion_matrix_means[3]]]).astype(int)

        sns.heatmap(confusion_matrix_means_2d_array, annot=True, cmap='Blues', fmt='g') # show values and avoid cientific notation
        plt.xlabel("Predicted label")
        plt.ylabel("True label")
        plt.show()
    
    return feature_coefficients

def sort_feature_importances(feature_coefficients):
    
    #Sort by descending order
    feature_coefficients = feature_coefficients.sort_values(by = "coefficients", ascending = False)
    feature_coefficients = feature_coefficients.reset_index(drop=True)
    
    return feature_coefficients