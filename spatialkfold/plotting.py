from typing import Union
import numpy as np
import pandas as pd
from sklearn.model_selection import LeaveOneGroupOut 
import matplotlib.pyplot as plt
import geopandas as gpd

def spatial_kfold_plot (X :Union[np.ndarray, pd.DataFrame, pd.Series], geometry :Union[pd.Series, pd.DataFrame], groups : Union[np.ndarray, pd.Series], fold_num , ax = None, **kwargs):
    
    """
    Generate a plot differentiating between the train and test data during the cross validation for a specific fold
    
    Parameters
    ----------
    X : pandas DataFrame
        The feature data.
    geometry : pd.DataFrame or pandas Series
        geometry 
    group : np.ndarray, pd.Series
       values in the column in X that defines the spatial resmaple groups.
    fold_num : int
        fold number
        
    Returns
    -------
    plt plot
        Plot illustrating the cross validation for specific fold..
    
    """
    n_folds= len(np.unique(list(groups.values)))
    
    if fold_num > n_folds: 
        raise ValueError(f"The provided humber of folds {fold_num} is out of range. The number of existing folds is equal to {n_folds}") 
        
    # Initialize the LeaveOneGroupOut  
    spatial_kfold = LeaveOneGroupOut()
    
    # Iterate over the training and testing indices
    for idx, (train_index, test_index) in enumerate(spatial_kfold.split(X, geometry, groups=groups)):
        if idx != (fold_num - 1):
            None
        elif idx == (fold_num - 1 ):
            X_train, X_test = geometry.loc[train_index], geometry.loc[test_index]
            gdf_train = gpd.GeoDataFrame(X_train)
            gdf_test = gpd.GeoDataFrame(X_test)

            # Add corresponding train - test
            gdf_train['folds'] = 'train'
            gdf_test['folds'] = 'test'

            # Combine as single gdf 
            gdf_cv = pd.concat([gdf_train, gdf_test])
                       
            if ax:
                show = False
            else:
                show = True
            ax = plt.gca()
            
            gdf_cv.plot(column='folds', legend=True, ax=ax,**kwargs)
            ax.set_title(f'Fold {idx + 1 }', fontweight='bold')

            # Show the plot if no axes object was provided
            if show:
                plt.show()


def spatial_kfold_autoplot (X: Union[np.ndarray, pd.DataFrame, pd.Series], geometry :Union[pd.Series, pd.DataFrame], groups : Union[np.ndarray, pd.Series] ,**kwargs):
    
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
        Plot illustrating the cross validation a spatially resampled data.
    
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