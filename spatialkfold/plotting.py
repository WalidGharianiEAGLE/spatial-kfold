from typing import Union
import numpy as np
import pandas as pd
from sklearn.model_selection import LeaveOneGroupOut 
import matplotlib.pyplot as plt
import geopandas as gpd


def spatial_kfold_plot (X: Union[np.ndarray, pd.DataFrame, pd.Series], geometry :Union[pd.Series, pd.DataFrame], groups : Union[np.ndarray, pd.Series] ,**kwargs):
    
    """
    Generate a plot differentiating between the train and test data during the cross validation at each fold
    
    Parameters
    ----------
    X : pandas DataFrame
        The feature data.
    geometry : pd.DataFrame or pandas Series
        geometry 
    group : np.ndarray, pd.Series
       values in the column in X that defines the spatial resmaple groups.
    
    Returns
    -------
    plt plot
        Plot illustrating the cross validation an spatially resampled data.
    
    """
    
    # Get n of folds    
    n_folds= len(np.unique(list(groups.values)))
    
    # Initialize the LeaveOneGroupOut  
    spatial_kfold = LeaveOneGroupOut()

    # Get the n of rows - columns for the subplots
    nrows = int(np.ceil(np.sqrt(n_folds)))
    ncols = int(np.ceil(n_folds / nrows))

    # set figure and subplots
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize = (10,0))
    #ax = plt.gcf()
    ax = ax.flatten()

    # customize the fig size 
    fig = plt.gcf()
    fig.set_size_inches(ncols * 4, nrows * 4)
 
    # Iterate over the training and testing indices 
    for idx, (train_index, test_index) in enumerate(spatial_kfold.split(X , geometry, groups=groups)):
        
        cv_train, cv_test = geometry.loc[train_index], geometry.loc[test_index]        
        gdf_train = gpd.GeoDataFrame(cv_train)
        gdf_test = gpd.GeoDataFrame(cv_test)

        # Add corresponding train - test
        gdf_train['folds'] = 'train'
        gdf_test['folds'] = 'test'

        # Combine as single gdf 
        gdf_cv = pd.concat([gdf_train, gdf_test])
                       
        # Plot the training and testing sets on separate subplots
        gdf_cv.plot(ax=ax[idx], column='folds', legend=True)
        ax[idx].set_title(f'Fold {idx + 1}', fontweight='bold')

    plt.show()