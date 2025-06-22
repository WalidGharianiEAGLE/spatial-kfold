# spatial-kfold
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![pypi](https://img.shields.io/pypi/v/spatial-kfold.svg)](https://pypi.org/project/spatial-kfold/)
[![Downloads](https://static.pepy.tech/badge/spatial-kfold)](https://pepy.tech/project/spatial-kfold)

spatial-kfold: A Python Package for Spatial Resampling Toward More Reliable Cross-Validation in Spatial Studies.

spatial-kfold is a python library for performing spatial resampling to ensure more robust cross-validation in spatial studies. It offers spatial clustering and block resampling technique with user-friendly parameters to customize the resampling. It enables users to conduct a "Leave Region Out" cross-validation, which can be useful for evaluating the model's generalization to new locations as well as improving the reliability of [feature selection](https://doi.org/10.1016/j.ecolmodel.2019.108815) and [hyperparameter tuning](https://doi.org/10.1016/j.ecolmodel.2019.06.002) in spatial studies.


spatial-kfold can be integrated easily with scikit-learn's [LeaveOneGroupOut](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.LeaveOneGroupOut.html) cross-validation technique. This integration enables you to further leverage the resampled spatial data for performing feature selection and hyperparameter tuning.

# Main Features

spatial-kfold allow conducting "Leave Region Out" using two spatial resampling techniques:

* 1. Spatial clustering with KMeans or BisectingKMeans
* 2. Spatial blocks (rect / hex)
    * Random blocks
    * Continuous blocks 
        * tb-lr : top-bottom, left-right
        * bt-rl : bottom-top, right-left

# Installation

spatial-kfold can be installed from [PyPI](https://pypi.org/project/spatial-kfold/)

```
pip install spatial-kfold
```

# Example 

## 1. Spatial clustering with KMeans [![View Jupyter Notebook](https://img.shields.io/badge/view-Jupyter%20notebook-lightgrey.svg)](https://github.com/WalidGharianiEAGLE/spatial-kfold/blob/main/notebooks/spatialkfold_intro.ipynb)

```python
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors as colors
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from spatialkfold.blocks import spatial_blocks 
from spatialkfold.datasets import load_ames
from spatialkfold.clusters import spatial_kfold_clusters 

# Load ames data
ames = load_ames()
ames_prj = ames.copy().to_crs(ames.estimate_utm_crs())
ames_prj['id'] = range(len(ames_prj))

# 1. Spatial cluster resampling 
ames_clusters = spatial_kfold_clusters(
  gdf=ames_prj, 
  name='id', 
  nfolds=10, 
  algorithm='kmeans', # "bisectingkmeans"
  n_init="auto", 
  random_state=569
  ) 

# Get the 'tab20' colormap
cols_tab = cm.get_cmap('tab20', 10)
# Generate a list of colors from the colormap
cols = [cols_tab(i) for i in range(10)]
# create a color ramp
color_ramp = ListedColormap(cols)


fig, ax = plt.subplots(1,1 , figsize=(9, 4)) 
ames_clusters.plot(column='folds', ax=ax, cmap= color_ramp, markersize = 2, legend=True)
ax.set_title('Spatially Clustered Folds\nUsing KMeans')
plt.show()
```

<p align="center">
  <img src="https://github.com/WalidGharianiEAGLE/spatial-kfold/blob/main/images/clusters_resampling.png?raw=true" width="400" />
</p>

## 2. Spatial blocks [![View Jupyter Notebook](https://img.shields.io/badge/view-Jupyter%20notebook-lightgrey.svg)](https://github.com/WalidGharianiEAGLE/spatial-kfold/blob/main/notebooks/spatialkfold_intro.ipynb)

```python

# 2.1 spatial resampled random blocks  

# create 10 random blocks 
ames_rnd_blocks = spatial_blocks(
  gdf=ames_prj, 
  width=1500, 
  height=1500, 
  method="random",     # "continuous"
  orientation="tb-lr", # "bt-rl"
  grid_type="rect",    # "hex" 
  random_state=135
  )

# resample the ames data with the prepared blocks 
ames_res_rnd_blk = gpd.overlay(ames_prj, ames_rnd_blocks)

# plot the resampled blocks
fig, ax = plt.subplots(1,2 , figsize=(10, 6)) 

# plot 1
ames_rnd_blocks.plot(column='folds',cmap=color_ramp, ax=ax[0] ,lw=0.7, legend=False)
ames_prj.plot(ax=ax[0],  markersize = 1, color = 'r')
ax[0].set_title('Random Blocks Folds')

# plot 2
ames_rnd_blocks.plot(facecolor="none",edgecolor='grey', ax=ax[1] ,lw=0.7, legend=False)
ames_res_rnd_blk.plot(column='folds', cmap=color_ramp, legend=False, ax=ax[1], markersize=3)
ax[1].set_title('Spatially Resampled\nrandom blocks')


im1 = ax[1].scatter(ames_res_rnd_blk.geometry.x , ames_res_rnd_blk.geometry.y, c=ames_res_rnd_blk['folds'], cmap=color_ramp, s=5)

axins1 = inset_axes(
    ax[1],
    width="5%",  # width: 5% of parent_bbox width
    height="50%",  # height: 50%
    loc="lower left",
    bbox_to_anchor=(1.05, 0, 1, 2),
    bbox_transform=ax[1].transAxes,
    borderpad=0
)
fig.colorbar(im1, cax=axins1,  ticks= range(1,11))

plt.show()
```

<p align="center">
  <img src="https://github.com/WalidGharianiEAGLE/spatial-kfold/blob/main/images/blocks_resampling.png?raw=true" width="700" />
</p>

## 3. Compare Random and Spatial cross validation [![View Jupyter Notebook](https://img.shields.io/badge/view-Jupyter%20notebook-lightgrey.svg)](https://github.com/WalidGharianiEAGLE/spatial-kfold/blob/main/notebooks/spatialkfold_intro.ipynb)

<p align="center">
  <img src="https://github.com/WalidGharianiEAGLE/spatial-kfold/blob/main/images/randomCV_spatialCV.png?raw=true" width="800" />
</p>

## 4 .Feature Selection with spatial-kfold

```python
from sklearn.feature_selection import RFECV
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import LeaveOneGroupOut

clf = RandomForestRegressor()
group_cvs = LeaveOneGroupOut()
spatial_folds = ames_clusters.folds.values.ravel()

rfecv = RFECV(estimator=clf, step=1, cv=group_cvs)
rfecv.fit(X, y, groups=spatial_folds)

```

## 5. Hyperparameter tuning with spatial-kfold

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import LeaveOneGroupOut, GridSearchCV

clf = RandomForestRegressor()
param_grid = {
    'n_estimators': [50, 100, 150],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5],
}
group_cvs = LeaveOneGroupOut()
spatial_folds = ames_clusters.folds.values.ravel()

grid_search = GridSearchCV(estimator=clf, param_grid=param_grid, cv=group_cvs)
grid_search.fit(X, y, groups=spatial_folds)
```

# Credits

This package was inspired by the following R packages:

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


# Citation

If you use My Package in your research or work, please cite it using the following entries:

- MLA Style:

```
Ghariani, Walid. "spatial-kfold: A Python Package for Spatial Resampling Toward More Reliable Cross-Validation in Spatial Studies." 2023. GitHub, https://github.com/WalidGharianiEAGLE/spatial-kfold
```
- BibTex Style:

```
@Misc{spatial-kfold,
author = {Walid Ghariani},
title = {spatial-kfold: A Python Package for Spatial Resampling Toward More Reliable Cross-Validation in Spatial Studies},
howpublished = {GitHub},
year = {2023},
url = {https://github.com/WalidGharianiEAGLE/spatial-kfold}
}
```
# Resources

A list of tutorials and resources mainly in R explaining the importance of spatial resampling and spatial cross validation

*  [Hanna Meyer: "Machine-learning based modelling of spatial and spatio-temporal data"](https://www.youtube.com/watch?v=QGjdS1igq78&t=1271s)
* [Jannes Münchow: "The importance of spatial cross-validation in predictive modeling"](https://www.youtube.com/watch?v=1rSoiSb7xbw&t=649s)
* [Julia Silge: Spatial resampling for more reliable model evaluation with geographic data ](https://www.youtube.com/watch?v=wVrcw_ek3a4&t=904s)

# Bibliography

Meyer, H., Reudenbach, C., Wöllauer, S., Nauss, T. (2019): Importance of spatial predictor variable selection in machine learning applications - Moving from data reproduction to spatial prediction. Ecological Modelling. 411. https://doi.org/10.1016/j.ecolmodel.2019.108815

Schratz, Patrick, et al. "Hyperparameter tuning and performance assessment of statistical and machine-learning algorithms using spatial data." Ecological Modelling 406 (2019): 109-120. https://doi.org/10.1016/j.ecolmodel.2019.06.002

Schratz, Patrick, et al. "mlr3spatiotempcv: Spatiotemporal resampling methods for machine learning in R." arXiv preprint arXiv:2110.12674 (2021). https://arxiv.org/abs/2110.12674

Valavi, Roozbeh, et al. "blockCV: An r package for generating spatially or environmentally separated folds for k-fold cross-validation of species distribution models." Biorxiv (2018): 357798. https://doi.org/10.1101/357798 
