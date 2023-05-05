from scipy import stats
import modules.exploratory_data_analysis.base_rates as base_rates

def t_test(df, var, var_group, alpha = 0.05):
    
    df_group1, df_group2 = base_rates.df_by_group(df, var_group)
    a = df_group1[var]
    b = df_group2[var]
    
    print("Unpaired/independent t-test to determine if there is significant difference between the two groups by quantifying the difference between the arithmetic means \n")
    
    t_statistic, p_value = stats.ttest_ind(a, b)

    print("------> T-statistic: " + str(t_statistic) + "\n")

    print("------> p-value: " + str(p_value) + "\n")

    if p_value <= alpha:
        print("Since p-value is smaller than alpha, we REJECT the null hypothesis H0. Thus, there is a significant difference between both groups")

    else:
        print("Since p-value is not smaller than alpha, we CANNOT reject the null hypothesis H0.")
        
        
def k_test(df, var, var_group, alpha = 0.05):
    
    df_group1, df_group2 = base_rates.df_by_group(df, var_group)
    a = df_group1[var]
    b = df_group2[var]
    
    print("Kolmogorov-Smirnov test to determine if there is significant difference between the two groups by quantifying the difference between the arithmetic means \n")
    
    statistic, p_value = stats.mannwhitneyu(a, b)

    print("------> Statistic: " + str(statistic) + "\n")

    print("------> p-value: " + str(p_value) + "\n")

    if p_value <= alpha:
        print("Since p-value is smaller than alpha, we REJECT the null hypothesis H0. Thus, there is a significant difference between both groups")

    else:
        print("Since p-value is not smaller than alpha, we CANNOT reject the null hypothesis H0.")