import numpy as np
from sklearn.preprocessing import MinMaxScaler

def scale(df, non_scalable_cols):   
    # Scale from 0 to 1 (good if no outliers and no need for a normal distribution)
    
    # Define cols to scale (avoid binary)
    binary_cols = [col for col in df if np.isin(df[col].unique(), [0, 1]).all()]
    cols = [i for i in df.columns if i not in binary_cols]
    cols = [i for i in cols if i not in non_scalable_cols]
    
    # Apply scaler
    scaler = MinMaxScaler()
    df.loc[:, cols] = scaler.fit_transform(df.loc[:,cols])
    
    return df

def null_values_detection(df):
    
    # Check if there are null values in the dataframe
    if df.isnull().values.any():
        print("Null values found in the dataset")
        
        # Detect the null values
        for column in df.columns:
            null_count = df[column].isnull().sum()
            if(null_count != 0):
                print("In column '" + str(column) + "' there are " + str(null_count) + " null values")   
    else:
        print("There are no null values in the dataset")
    