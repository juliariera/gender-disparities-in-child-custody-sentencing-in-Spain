import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from itertools import combinations

import modules.utils.utils as utils
import modules.data_wrangling.feature_selection as feature_selection

def euclidean_distance(a, b):
    dist = np.linalg.norm(a-b)
    return dist


def similarity_cols(features_classification_lists, show_removed_cols = False, show_cols_similarity = False):
        
    non_info_cols = features_classification_lists["Judicial resolution"]
    court_decicion_cols = features_classification_lists["Court decisions"]
    
    cols = utils.flatten_list_of_lists(features_classification_lists)
    
    cols_similarity = [i for i in cols if i not in (non_info_cols)]
    cols_similarity = [i for i in cols_similarity if i not in (court_decicion_cols)]
    
    if(show_removed_cols):
        removed_cols = [i for i in cols if i not in cols_similarity]
        print("The removed columns are:")
        print(removed_cols)
        
    if(show_cols_similarity):
        print("\nThe columns used for similarity are:")
        print(cols_similarity)
        
    return cols_similarity


def similarity_df(df, cols_similarity):
    df_similarity = df[df.columns.intersection(cols_similarity)]
    return df_similarity


def get_value_condensed_matrix(distances, i, j, m):
    pos = m * i + j - ((i + 2) * (i + 1)) // 2
    value = distances[pos]
    return value

def from_condensed_to_df(df, distances):
    
    distances_dict = [{'sentence_1':i, 'sentence_2':j, 'distance':get_value_condensed_matrix(distances, i, j, len(df))} 
                  for i, j in combinations(range(len(df)), 2)]
    
    df_distances = pd.DataFrame.from_records(distances_dict)
    
    return df_distances

def get_distances_df(df, weights = []):
    if(len(weights)==0):
        print("Euclidean")
        distances = pdist(df.values, metric='euclidean')
    else:
        print("Euclidean with weights")
        distances = pdist(df.values, metric='euclidean', w=weights)
        
    df_distances = from_condensed_to_df(df, distances)
    
    return df_distances


def distances_plot(distances_df):
    sns.distplot(distances_df["distance"], label="distance", color = "#e2b0a6")
    plt.title('Distances distribution')
    plt.legend()
    plt.show()
