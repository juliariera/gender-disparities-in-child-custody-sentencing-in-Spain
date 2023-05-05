import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statistics


def select_by_index(distances_df, indices):
    
    subset_distances_df = pd.DataFrame(columns = ["sentence_1", "sentence_2", "distance"])
    
    for index, row in distances_df.iterrows():
        
        sentence_1 = int(row["sentence_1"])
        sentence_2 = int(row["sentence_2"])
                
        if (sentence_1 in indices) and (sentence_2 in indices):
            subset_distances_df = subset_distances_df.append(row, ignore_index=True)
            
    subset_distances_df = subset_distances_df.astype({"sentence_1": int, "sentence_2": int, "distance": float})
    
    return subset_distances_df


def get_judge_sentences(df, judge_id):
    df = df[df["JUDGE_ID"] == judge_id]
    return df


def get_judge_distances(df, distances_df, judge_id):
    
    judge_sentences = get_judge_sentences(df, judge_id)
    indices = judge_sentences.index
    
    judge_distances_df = select_by_index(distances_df, indices)
            
    return judge_distances_df


def get_sentences_by_gender(df, gender):
    df = df[df["JUDGE_ML"] == gender]
    return df


def get_distances_by_gender(df, distances_df, gender):

    sentences = get_sentences_by_gender(df, gender)
    indices = sentences.index
    gender_distances_df = select_by_index(distances_df, indices)
            
    return gender_distances_df


def add_ICD_BCD_label_distances(df, distances_df):
    
    label_comparison = []
    
    for index, row in distances_df.iterrows():
                
        label_1 = df.loc[row["sentence_1"],"WINWIN"]
        label_2 = df.loc[row["sentence_2"],"WINWIN"]
                
        if(label_1 == 0) and (label_2 == 0):
            label_comparison.append("ICD_0")
            
        elif(label_1 == 1) and (label_2 == 1):
            label_comparison.append("ICD_1")
            
        else:
            label_comparison.append("BCD")
        
    distances_df["label_comparison"] = label_comparison
    
    return distances_df


def plot_distances_distribution(df, distances_df):
    
    # Add label
    distances_df = add_ICD_BCD_label_distances(df, distances_df)
    
    # Split    
    distances_df_ICD_0 = distances_df[distances_df["label_comparison"] == "ICD_0"]
    distances_df_ICD_1 = distances_df[distances_df["label_comparison"] == "ICD_1"]
    distances_df_BCD = distances_df[distances_df["label_comparison"] == "BCD"]

    # Plot
    sns.distplot(distances_df_ICD_0["distance"], label="distance ICD_0")
    sns.distplot(distances_df_ICD_1["distance"], label="distance ICD_1")
    sns.distplot(distances_df_BCD["distance"], label="distance BCD")
    plt.title('Distances distribution')
    plt.legend()
    plt.xlabel("distance")
    plt.ylabel("frequency")
    plt.show()
        
    # Print means
    mean_ICD_0 = statistics.mean(distances_df_ICD_0["distance"])
    mean_ICD_1 = statistics.mean(distances_df_ICD_1["distance"])
    mean_BCD = statistics.mean(distances_df_BCD["distance"])
    
    print("Mean for ICD_0 distribution: " + str(round(mean_ICD_0, 3)))
    print("Mean for ICD_1 distribution: " + str(round(mean_ICD_1, 3)))
    print("Mean for BCD distribution: " + str(round(mean_BCD, 3)))
    
    mean_ICD = statistics.mean([mean_ICD_0, mean_ICD_1])
    print("\nMean for both ICD distribution: "  + str(round(mean_ICD,3)))
    
    diff = mean_BCD - mean_ICD
    print("\nDifference between BCD mean and ICD mean: " + str(round(diff,3)))
    
