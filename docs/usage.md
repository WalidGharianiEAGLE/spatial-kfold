```py
import geopandas as gpd

from spatialkfold.datasets import load_ames
from spatialkfold.blocks import spatial_blocks 
from spatialkfold.clusters import spatial_kfold_clusters 
```

## Spatial cluster resampling 

```py
ames = load_ames()
ames_prj = ames.copy().to_crs(ames.estimate_utm_crs())
ames_prj['id'] = range(len(ames_prj))

ames_clusters = spatial_kfold_clusters(
  gdf=ames_prj, 
  name='id', 
  nfolds=10, 
  algorithm='kmeans', # "bisectingkmeans"
  n_init="auto", 
  random_state=569
  ) 
```

## Spatially resampled blocks  

```py
# create 10 random/continuous blocks 
ames_rnd_blocks = spatial_blocks(
  gdf=ames_prj, 
  width=1500, 
  height=1500, 
  method="random",     # "continuous"
  orientation="tb-lr", # "bt-rl"
  grid_type="rect",    # "hex" 
  nfolds=10, 
  random_state=135
  )

# resample the ames data with the prepared blocks 
ames_res_rnd_blk = gpd.overlay(ames_prj, ames_rnd_blocks) 
```