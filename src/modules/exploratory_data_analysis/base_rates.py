from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt

def percentage(df, var, boolean):
    return str(round((fraction(df, var, boolean))*100,2))

def fraction(df, var, boolean):
    return Counter(df[var])[boolean]/df.shape[0]    

def df_by_group(df, var_group):
    df_group1 = df[df[var_group] == 0]
    df_group2 = df[df[var_group] == 1]
    return df_group1, df_group2


def percentages(df, var, group_1, group_2, plot = True):
    
    print(Counter(df[var]))
    print("\n")
    
    print(str(group_1) + ": " + percentage(df, var, 0) + "%")
    print(str(group_2) + ": " + percentage(df, var, 1) + "%")
    print("\n")
    
    if plot:
        sns.countplot(x=var, data=df, palette=["#e2b0a6","#d0c7bd"])
        plt.title(str(group_1) + " vs " + str(group_2))
        plt.show()
    
def percentages_by_group(df, var, var_group, group_1, group_2, zero_case = False, group_1_zero = None, group_2_zero = None, plot = False):
    
    df_group1, df_group2 = df_by_group(df, var_group)

    # Group 1
    
    print(str(var_group) + " = 0 -->  " + str(var) + ": " + str(Counter(df_group1[var])) + "\n")

    if zero_case:
        print(str(group_1_zero) + ": " + percentage(df_group1, var, 0) + "%")
    
    print(str(group_1) + ": " + percentage(df_group1, var, 1) + "%")
    
    if plot:
        sns.countplot(x=var, data=df_group1, palette=["#e2b0a6","#d0c7bd"])
        plt.title(str(group_1_zero) + " vs " + str(group_1))
        plt.show()
        
    # Group 2
    
    print("\n" + str(var_group) + " = 1 -->  " + str(var) + ": " + str(Counter(df_group2[var])) + "\n")
    
    if zero_case:
        print(str(group_2_zero) + ": " + percentage(df_group2, var, 0) + "%")
    
    print(str(group_2) + ": " + percentage(df_group2, var, 1) + "%")
    
    if plot:
        sns.countplot(x=var, data=df_group2, palette=["#e2b0a6","#d0c7bd"])
        plt.title(str(group_2_zero) + " vs " + str(group_2))
        plt.show()
            
def ratio_by_group(df, var, var_group, group1, group2):
    
    df_group1, df_group2 = df_by_group(df, var_group)
    
    # Ratio between group 1 and group 2 for var = 0
    ratio_zero  = fraction(df_group1, var, 0)/fraction(df_group2, var, 0)
    print(str(var) + " = 0 -->  " + "Ratio between " + str(group1) + "/" + str(group2) + " is: " +  str(round(ratio_zero,2)))
    
    # Ratio between group 1 and group 2 for var = 1
    ratio_one  = fraction(df_group1, var, 1)/fraction(df_group2, var, 1)
    print(str(var) + " = 1 -->  " + "Ratio between " + str(group1) + "/" + str(group2) + " is: " +  str(round(ratio_one,2)))
    
def select_by_two_vars(df, group_1_var, group_2_var, group_1_value, group_2_value): 
    df_selected = df.loc[((df[group_1_var] == group_1_value) & (df[group_2_var] == group_2_value))]
    return df_selected

def percentages_cross_groups(df, var, group_1_var, group_2_var, group_1_value_0, group_1_value_1, group_2_value_0, group_2_value_1, counter = False):
    
    # Get the subgroups
    _0_0_selection = select_by_two_vars(df, group_1_var, group_2_var, 0, 0)
    _0_1_selection = select_by_two_vars(df, group_1_var, group_2_var, 0, 1)
    _1_0_selection = select_by_two_vars(df, group_1_var, group_2_var, 1, 0)
    _1_1_selection = select_by_two_vars(df, group_1_var, group_2_var, 1, 1)
    
    # Print the counter
    if(counter):
        print("For " + str(group_1_value_0) + ", "+ str(group_2_value_0) + " --> " + str(var) + ": " + str(Counter(_0_0_selection[var])))
        print("For " + str(group_1_value_0) + ", "+ str(group_2_value_1) + " --> " + str(var) + ": " + str(Counter(_0_1_selection[var])))
        print("For " + str(group_1_value_1) + ", "+ str(group_2_value_0) + " --> " + str(var) + ": " + str(Counter(_1_0_selection[var])))
        print("For " + str(group_1_value_1) + ", "+ str(group_2_value_1) + " --> " + str(var) + ": " + str(Counter(_1_1_selection[var])) + "\n")
    
    # Print the percentages
    print(str(var) + " percentage for " + str(group_1_value_0) + ", "+ str(group_2_value_0) + " --> " + str(percentage(_0_0_selection, var, 1)) + "%")
    print(str(var) + " percentage for " + str(group_1_value_0) + ", "+ str(group_2_value_1) + " --> " + str(percentage(_0_1_selection, var, 1)) + "%")
    print(str(var) + " percentage for " + str(group_1_value_1) + ", "+ str(group_2_value_0) + " --> " + str(percentage(_1_0_selection, var, 1)) + "%")
    print(str(var) + " percentage for " + str(group_1_value_1) + ", "+ str(group_2_value_1) + " --> " + str(percentage(_1_1_selection, var, 1)) + "%")
    
    
    
    

   
        