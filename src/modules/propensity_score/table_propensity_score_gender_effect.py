import modules.propensity_score.propensity_score as propensity_score

from tabulate import tabulate

def get_male_count(df_bucket, var):
    return len(df_bucket[df_bucket[var] == 1])

def get_female_count(df_bucket, var):
    return len(df_bucket[df_bucket[var] == 0])
    
def get_male_minus_female_count(df_bucket, var):
    return get_male_count(df_bucket, var) - get_female_count(df_bucket, var)
    
    
def create_table_3_buckets(df, var):
    
    df_list = propensity_score.get_equal_buckets(df, 'conf_1', 3)
    
    data = [["Low", get_male_count(df_list[0], var), get_female_count(df_list[0], var), get_male_minus_female_count(df_list[0], var)], 
            ["Medium", get_male_count(df_list[1], var), get_female_count(df_list[1], var), get_male_minus_female_count(df_list[1], var)], 
            ["High", get_male_count(df_list[2], var), get_female_count(df_list[2], var), get_male_minus_female_count(df_list[2], var)]]

    col_names = ["Propensity score bucket", "Male", "Female", "Effect"]
    
    print(tabulate(data, headers=col_names))