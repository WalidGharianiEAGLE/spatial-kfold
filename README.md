# spatial-kfold

spatial resampling for more robust cross validation in spatial studies

spatial-kfold is a python library for performing spatial resampling to ensure more robust cross-validation in spatial studies. It offers spatial clustering and block resampling technique with  user-friendly parameters to customize the resampling. It enables users to conduct a "Leave Region Out" cross-validation, which can be useful for evaluating the model's generalization to new locations as well as improving the reliability of [feature selection](https://doi.org/10.1016/j.ecolmodel.2019.108815) and [hyperparameter tuning](https://doi.org/10.1016/j.ecolmodel.2019.06.002) in spatial studies


Spatial-kfold can be integrated easily with scikit-learn's [LeaveOneGroupOut](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.LeaveOneGroupOut.html) cross-validation technique. This integration enables you to further leverage the resampled spatial data for performing feature selection and hyperparameter tuning.

# Main Features

spatial-kfold allow to conduct "Leave Region Out" using two spatial resampling techniques:

* 1. Spatial clustering with kmeans
* 2. Spatial blocks
    * Random blocks
    * Continuous blocks 
        * tb-lr : top-bottom, left-right
        * bt-rl : bottom-top, right-left

# Installation

spatial-kfold can be installed from [PyPI](https://pypi.org/project/spatial-kfold/)

```
pip install spatial-kfold
```

# Resources

A list of tutorials and resources mainly in R explaining the importance of saptial resampling and spatial cross validation

*  [Hanna Meyer: "Machine-learning based modelling of spatial and spatio-temporal data"](https://www.youtube.com/watch?v=QGjdS1igq78&t=1271s)
* [Jannes Münchow: "The importance of spatial cross-validation in predictive modeling"](https://www.youtube.com/watch?v=1rSoiSb7xbw&t=649s)
* [Julia Silge: Spatial resampling for more reliable model evaluation with geographic data ](https://www.youtube.com/watch?v=wVrcw_ek3a4&t=904s)

# Credits

This package was inspired by the following R packages.

* [CAST](https://github.com/HannaMeyer/CAST/)
* [spatialsample](https://github.com/tidymodels/spatialsample/) 

# Dependencies

This project relies on the following dependencies:
* [pandas](https://pandas.pydata.org)
* [numpy](https://numpy.org)
* [geopandas](https://geopandas.org)
* [shapely](https://shapely.readthedocs.io)
* [matplotlib](https://matplotlib.org)
* [scikit-learn](https://scikit-learn.org)