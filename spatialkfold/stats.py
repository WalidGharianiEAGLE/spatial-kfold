from typing import Union

import numpy as np
import pandas as pd
from sklearn.model_selection import LeaveOneGroupOut


def spatial_kfold_stats(
    X: Union[np.ndarray, pd.DataFrame, pd.Series],
    y: Union[np.ndarray, pd.Series, pd.DataFrame],
    groups: Union[np.ndarray, pd.Series],
):
    """
    Generate a DataFrame with the number of train and test samples in each split of a spatial resampling procedure.

    Parameters
    ----------
    X : np.ndarray or pd.DataFrame or pd.Series
        The feature data.
    y : np.ndarray or pd.Series or pd.DataFrame
        The target values.
    group : np.ndarray or pd.Series
       values in the column in X that defines the spatially resmapled groups.

    Returns
    -------
    pandas DataFrame
        A DataFrame with the number of train and test samples in each split of the spatial resampling procedure.

    This function uses LeaveOneGroupOut from the scikit-learn documentation to ensure a leave-location-out” (LLO) procedure
    over a predifined group of folds:
     >> Each Group of clustered, blocked or user defined locations are used during the testing
        https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.LeaveOneGroupOut.html
    """
    df_list = {"split": [], "train": [], "test": []}
    spatial_kfold = LeaveOneGroupOut()

    for idx, (train_index, test_index) in enumerate(
        spatial_kfold.split(X, y=None, groups=groups)
    ):
        if isinstance(X, pd.DataFrame):
            X_train, X_test = X.loc[train_index], X.loc[test_index]
        elif isinstance(X, pd.Series):
            X_train, X_test = X.loc[train_index], X.loc[test_index]
        else:
            X_train, X_test = X[train_index], X[test_index]
        df_list["split"].append(idx + 1)
        df_list["train"].append(len(X_train))
        df_list["test"].append(len(X_test))
        kfold_splits = pd.DataFrame(df_list)

    return kfold_splits
