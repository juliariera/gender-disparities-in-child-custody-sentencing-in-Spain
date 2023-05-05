import pandas as pd

def get_df_categories(file_name):
    return pd.read_csv(file_name, sep=";")

def get_list_categories(file_name):
    df_categories = get_df_categories(file_name)
    list_categories = list(pd.unique(df_categories['category']))
    return list_categories

def categories_list_and_dict(file_name=r"..\data\feature_category.csv"):
    
    # Get data 
    df_feature_category = get_df_categories(file_name)

    # Get the categories list
    categories_list = get_list_categories(file_name)
    
    # Convert to dict
    dict_feature_category = {}

    for index, row in df_feature_category.iterrows():
        dict_feature_category[row["feature"]] = row["category"]

    return categories_list, dict_feature_category