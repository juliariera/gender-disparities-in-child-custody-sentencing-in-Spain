import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score

import modules.exploratory_data_analysis.base_rates as base_rates
import modules.utils.utils as utils

def mean_prob_by_group(df, df_conf, group_var):
    
    # Add group variable to the confidence dataset
    df_conf[group_var] = df[group_var]
    
    # Split the dataset by group
    df_conf_group_1, df_conf_group_2 = base_rates.df_by_group(df_conf, group_var)
    
    # Get means
    group_1_mean = df_conf_group_1["conf_1"].mean()
    group_2_mean = df_conf_group_2["conf_1"].mean()
    
    return group_1_mean, group_2_mean
    

def conf_by_index(df_conf):
    df_conf = df_conf.reindex(df_conf["test_index"].sort_values(ascending=True).index).reset_index(drop=True)
    return df_conf

def rf_classifier_conf(df, target_var, hide_cols):
    clf = RandomForestClassifier(n_estimators = 1000)
    return classifier_get_conf(clf, df, target_var, hide_cols)

def lr_classifier_conf(df, target_var, hide_cols):
    clf = LogisticRegression(random_state=0, C=1, max_iter=1000, solver='lbfgs')
    return classifier_get_conf(clf, df, target_var, hide_cols)

def classifier_get_conf(clf, df, target_var, hide_cols):
    
    # Prepare the data
    cols = [i for i in df.columns if i not in (target_var)]
    cols = [i for i in cols if i not in (hide_cols)]
    X = df[cols].to_numpy()
    y = df[target_var].to_numpy()

    # Create a cross validator with 5 splits
    cv = StratifiedKFold(n_splits=5)
    cv.get_n_splits(X, y)

    balanced_accuracy_list = []
    test_index_list = []
    conf_1_list = []
    
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
        
        # Confidence: Get the index and confidence of 1 
        test_index_list.append(list(test_index))
        conf_1_list.append(list(y_prob[:,1]))
        
    
    # Performance: mean
    print("Balanced accuracy mean: " + str(np.mean(balanced_accuracy_list)))
    
    # Confidence: create a dataframe   
    flat_test_index_list = utils.flatten_list_of_lists(test_index_list)
    flat_conf_1_list = utils.flatten_list_of_lists(conf_1_list)
    
    df_conf = pd.DataFrame(list(zip(flat_test_index_list, flat_conf_1_list)),
               columns =['test_index', 'conf_1'])

    return df_conf