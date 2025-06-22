# spatial-kfold

[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![pypi](https://img.shields.io/pypi/v/spatial-kfold.svg)](https://pypi.org/project/spatial-kfold/)
[![Downloads](https://static.pepy.tech/badge/spatial-kfold)](https://pepy.tech/project/spatial-kfold)

---
spatial-kfold: A Python Package for Spatial Resampling Toward More Reliable Cross-Validation in Spatial Studies.

spatial-kfold is a python library for performing spatial resampling to ensure more robust cross-validation in spatial studies. It offers spatial clustering and block resampling technique with user-friendly parameters to customize the resampling. It enables users to conduct a "Leave Region Out" cross-validation, which can be useful for evaluating the model's generalization to new locations as well as improving the reliability of [feature selection](https://doi.org/10.1016/j.ecolmodel.2019.108815) and [hyperparameter tuning](https://doi.org/10.1016/j.ecolmodel.2019.06.002) in spatial studies.


spatial-kfold can be integrated easily with scikit-learn's [LeaveOneGroupOut](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.LeaveOneGroupOut.html) cross-validation technique. This integration enables you to further leverage the resampled spatial data for performing feature selection and hyperparameter tuning.

---

## Features

- Conduct *Leave Region Out* using two spatial resampling techniques:
  - Spatial clustering with **KMeans** or **BisectingKMeans**
  - Spatial blocks
    - Random blocks
    - Continuous blocks

      - `tb-lr` (top-bottom, left-right)
      - `bt-rl` (bottom-top, right-left)

- Integrates easily with scikit-learn’s `LeaveOneGroupOut` cross-validation to enable advanced feature selection and hyperparameter tuning.

---

## Installation

You can install **spatial-kfold** directly from PyPI:

```bash
pip install spatial-kfold
```

---

## Credits

This package was inspired by the following R packages:

* [CAST](https://github.com/HannaMeyer/CAST/)
* [spatialsample](https://github.com/tidymodels/spatialsample/) 

---

## Dependencies

This project relies on the following dependencies:

- [pandas](https://pandas.pydata.org)
- [numpy](https://numpy.org)
- [geopandas](https://geopandas.org)
- [shapely](https://shapely.readthedocs.io)
- [matplotlib](https://matplotlib.org)
- [scikit-learn](https://scikit-learn.org)

---

## Citation

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

---

## Resources

A list of tutorials and resources mainly in R explaining the importance of spatial resampling and spatial cross validation

*  [Hanna Meyer: "Machine-learning based modelling of spatial and spatio-temporal data"](https://www.youtube.com/watch?v=QGjdS1igq78&t=1271s)
* [Jannes Münchow: "The importance of spatial cross-validation in predictive modeling"](https://www.youtube.com/watch?v=1rSoiSb7xbw&t=649s)
* [Julia Silge: Spatial resampling for more reliable model evaluation with geographic data ](https://www.youtube.com/watch?v=wVrcw_ek3a4&t=904s)

---

## Bibliography

Meyer, H., Reudenbach, C., Wöllauer, S., Nauss, T. (2019): Importance of spatial predictor variable selection in machine learning applications - Moving from data reproduction to spatial prediction. Ecological Modelling. 411. https://doi.org/10.1016/j.ecolmodel.2019.108815

Schratz, Patrick, et al. "Hyperparameter tuning and performance assessment of statistical and machine-learning algorithms using spatial data." Ecological Modelling 406 (2019): 109-120. https://doi.org/10.1016/j.ecolmodel.2019.06.002

Schratz, Patrick, et al. "mlr3spatiotempcv: Spatiotemporal resampling methods for machine learning in R." arXiv preprint arXiv:2110.12674 (2021). https://arxiv.org/abs/2110.12674

Valavi, Roozbeh, et al. "blockCV: An r package for generating spatially or environmentally separated folds for k-fold cross-validation of species distribution models." Biorxiv (2018): 357798. https://doi.org/10.1101/357798 

---


