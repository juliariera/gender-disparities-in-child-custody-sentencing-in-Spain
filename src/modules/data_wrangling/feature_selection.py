import pandas as pd

def features_classification_lists(file_name=r"..\..\data\features_classification.csv"):
    features_classification_df = pd.read_csv(file_name, sep=";")
    features_classification_lists = features_classification_df.groupby('Group')['Short name'].apply(list)
    return features_classification_lists

def select_dataset_features(df, features_classification_lists, added_features_list, show_removed_cols=False):
    
    # Get the list of desired features
    lists = features_classification_lists
    list_features = lists["Judicial resolution"]+added_features_list+lists["Judge gender"]+lists["Plainfiff's gender"]+lists["Defendants's gender"]+lists["Plainfiff's requests"]+lists["Legal principles"]+lists["Facts"]+lists["Legal norms"]+lists["Court decisions"]
    
    # Select features in the dataset
    df_old = df
    df = df[list_features]

    #Print the removed cols
    if(show_removed_cols):
        removed_cols = [i for i in df_old.columns if i not in df.columns]
        print("The removed columns are:")
        print(removed_cols)
    
    return df