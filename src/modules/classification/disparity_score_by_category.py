import pandas as pd
import numpy as np

import modules.data_preparation.categories as categories
import modules.data_wrangling.feature_selection as feature_selection

def define_valid_features():
    lists = feature_selection.features_classification_lists()
    valid_features = lists["Legal principles"] + lists["Facts"]    
    return valid_features

def score_by_category(df, dict_feature_by_category, col_name, valid_features):
    
    # Create a dict with each category and a list of all the values in that category
    dict_score_by_category = {}

    for index, row in df.iterrows():

        feature = row["features"]
        
        if feature in valid_features:
            score = row[col_name]
            category = dict_feature_by_category[feature]

            if category not in dict_score_by_category:
                dict_score_by_category[category] = []

            dict_score_by_category[category].append(score)

    # Create a dict with each category and the mean of all the values of that category
    dict_score_by_category_mean = {}

    for category in dict_score_by_category:
        dict_score_by_category_mean[category] = np.mean(dict_score_by_category[category])
        
    # Convert to list
    list_score_by_category = list(dict_score_by_category_mean.values())
    
    return list_score_by_category 


def create_categories_score_df(df, file_name=r"..\data\feature_category.csv"):
    
    # Define valid features, categories list and the feature category dictionary
    valid_features = define_valid_features()
    categories_list, dict_feature_category = categories.categories_list_and_dict(file_name)
    
    # Get score lists for coefficients_x, coefficients_y and disp_score
    coefficients_x_by_category_list = score_by_category(df, dict_feature_category, "coefficients_x", valid_features)
    coefficients_y_by_category_list = score_by_category(df, dict_feature_category, "coefficients_y", valid_features)
    disp_score_by_category_list = score_by_category(df, dict_feature_category, "disp_score", valid_features)
        
    # Convert to dataframe
    df_score_by_category = pd.DataFrame(list(zip(categories_list, coefficients_x_by_category_list, coefficients_y_by_category_list, disp_score_by_category_list)),
               columns =['category', 'coefficients_x_mean', 'coefficients_y_mean', 'disp_score_mean'])
    
    # Sort by absolute value of the disparity score for each feature type
    df_score_by_category = df_score_by_category.reindex(df_score_by_category["disp_score_mean"].abs().sort_values(ascending=False).index).reset_index(drop=True)
    
    return df_score_by_category
    