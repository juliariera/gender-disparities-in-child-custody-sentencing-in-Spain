import pandas as pd

def disp_score_feature_importance(feature_importance_1, feature_importance_2):
    
    # Merge the two datasets
    df_feature_importance = (pd.merge(feature_importance_1,feature_importance_2,left_index= True, right_index= True, how = "left", on='features'))
    df_feature_importance = df_feature_importance[["features", "coefficients_x", "coefficients_y"]]
    
    # Create a new score variable 
    df_feature_importance["disp_score"] = df_feature_importance["coefficients_x"] - df_feature_importance["coefficients_y"]
    
    # Sort by absolute value of the disparuty score 
    df_feature_importance = df_feature_importance.reindex(df_feature_importance["disp_score"].abs().sort_values(ascending=False).index)
    df_feature_importance = df_feature_importance.reset_index(drop=True)
    
    return df_feature_importance    


def disp_score_feature_importance_show_above_threshold(df_feature_importance, threshold = 0.01):
    
    df_feature_importance = df_feature_importance[df_feature_importance["disp_score"] > threshold]
    
    return df_feature_importance