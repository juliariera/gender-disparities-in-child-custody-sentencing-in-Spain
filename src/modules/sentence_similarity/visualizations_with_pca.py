import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches

from sklearn.decomposition import PCA


def apply_pca(df, cols_pca, n_comp=2):
    
    df_pca = df[df.columns.intersection(cols_pca)]
    
    pca = PCA(n_components=n_comp)
    pca.fit(df_pca)
    
    columns = ['pca_%i' % i for i in range(n_comp)]
    df_pca = pd.DataFrame(pca.transform(df_pca), columns=columns, index=df_pca.index)
    df_pca.head()
    
    # Add winwin column
    df_pca['label'] = df['WINWIN']
    
    return df_pca


def plot_df_pca(df_pca):
    
    colormap = np.array(['#660066', '#FFE842'])
    
    plt.scatter(df_pca['pca_0'], df_pca['pca_1'], c=colormap[df_pca['label']])
    
    lose = mpatches.Patch(color=colormap[0], label='Lose')
    win = mpatches.Patch(color=colormap[1], label='Win')
    
    plt.legend(handles=[lose,win], loc='upper left')
    
    plt.show()