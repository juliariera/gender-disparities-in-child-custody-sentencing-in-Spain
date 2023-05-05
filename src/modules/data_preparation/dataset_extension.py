import pandas as pd

def insert_column(df, after_column, column_name, add_list):
    
    idx = df.columns.get_loc(after_column) + 1
    df.insert(loc=idx, column=column_name, value=add_list)
    
    return df

def create_judge_map(judge_name_list):
    judge_map = {}
    judge_id = 0

    for judge_name in judge_name_list:
        if judge_name not in judge_map:
            judge_map[judge_name] = judge_id
            judge_id += 1

    return judge_map

def create_judge_id_list(judge_name_list, debug = False):
    
    judge_map = create_judge_map(judge_name_list)
    
    if debug:
        print(judge_map)
    
    judge_id_list = []

    for judge_name in judge_name_list:
        judge_id = judge_map[judge_name]
        judge_id_list.append(judge_id)

    return judge_id_list
    

def standarize_headquarters_names(df):
    
    df["HQ"].replace({"Alicante/Alacant": "Alicante", "Elche/Elx": "Elche", "Castellón de la Plana/Castelló de la Plana": "Castellón de la Plana", "Pamplona/Iruña": "Pamplona", "Donostia-San Sebastián": "San Sebastián", "Vitoria-Gasteiz": "Vitoria"}, inplace = True)

    return df

def add_autonomous_community(df):
    
    # Read csv with headquarters vs autonomous community relation
    hq_aut_comm = pd.read_csv("..\data\hq_aut_comm.csv", sep=";")
    
    # Create a dictionary with key: headquarters, value: autonomous community
    hq_aut_comm_dict = pd.Series(hq_aut_comm["AUT_COMM"].values,index=hq_aut_comm["HQ"]).to_dict()
    
    # Prepare the autonomous community column
    aut_comm_list = []
    for index, row in df.iterrows():
        aut_comm_list.append(hq_aut_comm_dict[row['HQ']])
        
    # Add the autonomous community column
    insert_column(df, "HQ", "AUT_COMM", aut_comm_list)
    
    return df
    