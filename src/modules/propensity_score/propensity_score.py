import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Get buckets

def get_equal_buckets(df, column, num_buckets):
    
    # Sort values
    df = df.sort_values(by=column, ascending=True)
    
    # Get num_buckets lists with equal size
    df_list = np.array_split(df, num_buckets)
    
    return df_list


# Get male percentage

def get_male_percentage_bucket(df, df_bucket, var):
    if(len(df_bucket) != 0 ):
        #percentage = len(df_bucket[df_bucket[var] == 1]) - len(df_bucket[df_bucket[var] == 0])
        average_males = len(df_bucket[df_bucket[var] == 1])/len(df_bucket)
        average_females = len(df_bucket[df_bucket[var] == 0])/len(df_bucket)
        ratio_males_females = average_males/average_females
        percentage = ratio_males_females/len(df)
    else:
        percentage = 0
    return percentage


def get_male_percentages(df, var, num_buckets):

    df_list = get_equal_buckets(df, 'conf_1', num_buckets)
    
    male_percentage = []
    
    for i in range(num_buckets):
        male_percentage.append(get_male_percentage_bucket(df, df_list[i], var))
    
    return male_percentage


# Confounding plot    

def counfounding_plot(male_percentage, num_buckets):
    confounding_df = pd.DataFrame(columns = ['bucket', 'male percentage'])

    bucket_ids = list(np.arange(1,num_buckets+1))    

    confounding_df['Winning probability'] = bucket_ids
    confounding_df['Gender effect'] = male_percentage #diff (# males - # females)

    sns.barplot(x="Winning probability", y="Gender effect", data=confounding_df, palette="pastel") #more winning prob, more prob being male
    plt.title("Confounding Evidence")
    
