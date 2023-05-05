import pandas as pd

import modules.data_preparation.categories as categories

from importlib import reload
categories = reload(categories)

def get_summary_features(df):
    
    features = []
    
    for index, row in df.iterrows():

        feature = row["feature"]

        if (str(feature) + "_b" in features) or (feature.replace("_b", "") in features):

            df = df.drop(index)

        features.append(feature)
    
    return df


def get_two_sentences_diference(df_original, df, index_1, index_2, cols_diff, categorical_cols, summary = False):
    
    print("-------- SENTENCES INFO --------")
    
    print("\nSentence " + str(index_1) + ":")
    print("--> Request joint: " + str(df.loc[index_1,"RQ_JOINT"]))
    print("--> Plaintiff gender: " + str(df.loc[index_1,"PLAIN_ML"]))
    print("--> Winwin label: " + str(df.loc[index_1,"WINWIN"]))
    
    print("\nSentence " + str(index_2) + ":")
    print("--> Request joint: " + str(df.loc[index_2,"RQ_JOINT"]))
    print("--> Plaintiff gender: " + str(df.loc[index_2,"PLAIN_ML"]))
    print("--> Winwin label: " + str(df.loc[index_2,"WINWIN"]))

    
    print("\n-------- SENTENCES DIFFERENCES --------")
    
    df_differences = pd.DataFrame(columns = ["feature", "sentence "+str(index_1), "sentence "+str(index_2), "difference"])
    
    for col in df.columns:
        if col in cols_diff:
            
            value_sentence_1 = df.loc[index_1,col]
            value_sentence_2 = df.loc[index_2,col]
                        
            if(value_sentence_1 != value_sentence_2):
                
                if col not in categorical_cols:
                
                    value_sentence_1 = round(value_sentence_1, 3)
                    value_sentence_2 = round(value_sentence_2, 3)
                    diff = round(abs(value_sentence_1 - value_sentence_2), 3)
                    
                    original_value_1 = df_original.loc[index_1,col]
                    original_value_2 = df_original.loc[index_2,col]
                    
                    value_1 = str(value_sentence_1) + " (" + str(original_value_1) + ")"
                    value_2 = str(value_sentence_2) + " (" + str(original_value_2) + ")"

                    new_row = {'feature':col, "sentence "+str(index_1): value_1, "sentence "+str(index_2): value_2, 'difference':diff}

                    df_differences = df_differences.append(new_row, ignore_index=True)
                    
                else:
                    
                    if (col == "JUDGE_ID"):
                        
                        judge_gender_1 =  df.loc[index_1,"JUDGE_ML"]
                        judge_gender_2 =  df.loc[index_2,"JUDGE_ML"]
                        
                        if(judge_gender_1 == 0): 
                            judge_gender_1 = "F"
                        else:
                            judge_gender_1 = "M"
                            
                        if(judge_gender_2 == 0): 
                            judge_gender_2 = "F"
                        else:
                            judge_gender_2 = "M"
                        
                        value_1 = str(value_sentence_1) + " (" + str(judge_gender_1) + ")"
                        value_2 = str(value_sentence_2) + " (" + str(judge_gender_2) + ")"
                        
                        new_row = {'feature':col, "sentence "+str(index_1): value_1, "sentence "+str(index_2): value_2, 'difference':"-"}
                        
                    else:                    
                        new_row = {'feature':col, "sentence "+str(index_1): value_sentence_1, "sentence "+str(index_2): value_sentence_2, 'difference':"-"}

                    df_differences = df_differences.append(new_row, ignore_index=True)
                    
    if summary:
        df_differences = get_summary_features(df_differences)
                                    
    return df_differences



def get_top_n_sentences_diference(df, df_similar_different_label, cols_diff, n = 10, summary = False):

    differences_dict = {}

    for index, row in df_similar_different_label.iterrows():
        if index < n:
            index_1 = int(row["sentence_1"])
            index_2 = int(row["sentence_2"])

            # Create a dict of frequencies
            for col in df.columns:
                if col in cols_diff:

                    value_sentence_1 = df.loc[index_1,col]
                    value_sentence_2 = df.loc[index_2,col]

                    if(value_sentence_1 != value_sentence_2):

                        if col not in differences_dict:
                            differences_dict[col] = 1
                        else:
                            differences_dict[col] += 1 
                                                        
            # Convert to dataframe
            differences_df = pd.DataFrame(columns = ["feature", "frequency"])

            for key in differences_dict:
                new_row = {"feature": key, "frequency": differences_dict[key]}
                differences_df = differences_df.append(new_row, ignore_index=True)

            # Sort by descending order
            differences_df = differences_df.sort_values(by = "frequency", ascending = False)
            differences_df = differences_df.reset_index(drop=True)
            
    if summary:
        differences_df = get_summary_features(differences_df)

    return differences_df


def dict_feature_group_diff(file_name=r"..\data\feature_category.csv"):
    
    categories_list, dict_feature_category = categories.categories_list_and_dict(file_name)
    
    # List groups
    diff_groups_list = categories_list + ["Gender", "Judge", "Requests", "Location"]
    diff_groups_list
    
    # Dict feature group
    dict_feature_group = dict_feature_category

    dict_feature_group["DEFEN_ML"] = "Gender"
    dict_feature_group["PLAIN_ML"] = "Gender"
    dict_feature_group["JUDGE_ML"] = "Gender"

    dict_feature_group["JUDGE_ID"] = "Judge"

    dict_feature_group["RQ_JOINT"] = "Requests"
    dict_feature_group["RQ_FH_AT"] = "Requests"
    dict_feature_group["RQ_FH_SP"] = "Requests"
    dict_feature_group["RQ_MP_AT"] = "Requests"
    dict_feature_group["RQ_MP_SP"] = "Requests"

    dict_feature_group["AUT_COMM"] = "Location"
    
    return diff_groups_list, dict_feature_group


def get_top_n_sentences_diference_by_group(df, df_similar_different_label, cols_diff, n = 10, file_name=r"..\data\feature_category.csv"):
    
    differences_df  = get_top_n_sentences_diference(df, df_similar_different_label, cols_diff, n)
    
    diff_groups_list, dict_feature_group = dict_feature_group_diff(file_name)

    group_differences_dict = {}

    features = []
    
    for index, row in differences_df.iterrows():
        
        feature = row["feature"]
                
        if (str(feature) + "_b" not in features) and (feature.replace("_b", "") not in features):

            group = dict_feature_group[feature]

            if group not in group_differences_dict:
                group_differences_dict[group] = row["frequency"]
            else:
                group_differences_dict[group] += row["frequency"] 
                                
        features.append(feature)
            
    # Convert to dataframe
    group_differences_df = pd.DataFrame(columns = ["feature group", "frequency"])

    for key in group_differences_dict:
        new_row = {"feature group": key, "frequency": group_differences_dict[key]}
        group_differences_df = group_differences_df.append(new_row, ignore_index=True)

    # Sort by descending order
    group_differences_df = group_differences_df.sort_values(by = "frequency", ascending = False)
    group_differences_df = group_differences_df.reset_index(drop=True)

    return group_differences_df



