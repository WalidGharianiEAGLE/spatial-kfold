import geopandas as gpd
from sklearn.cluster import KMeans

def spatial_kfold_clusters (gdf, name, nfolds, random_state = None, **kwargs) :
    
    """
    Perform a spatial clustering using KMeans on a GeoDataFrame with coordinates and assign each geo point to a fold 
    
    Parameters
    ----------
    gdf : GeoDataFrame
        The GeoDataFrame with a geometry column containing the points to use for the spatial clustering.
     name : str
        name of the column that identify each unique geospatial point. eg: station_id or city_code 
    nfolds : int
        The number of clusters/folds to assign for each geospatial point.
    kwargs : set of arguments tp provide for kmeans from sklean api : https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
            eg: algorithm {“lloyd”, “elkan”, “auto”, “full”}, default=”lloyd”

    random_state : int, optional
        An optional integer seed to use  for centroid initialization. 
    
    Returns
    -------
    GeoDataFrame
        A GeoDataFrame containing with a 'groups' column.
 
    """
    # Check that the input is a GeoDataFrame
    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError('Input must be a GeoDataFrame')

    # Check the crs of the GeoDataFrame
    if (gdf.crs == None):
        raise AttributeError('The passed GeoDataFrame has no CRS. Use `to_crs()` to reproject one of the input geometries.')
        
    gdf_copy = gdf.reset_index().copy().drop(columns = ['index'])    
    gdf_copy['lon'] = gdf_copy['geometry'].x
    gdf_copy['lat'] = gdf_copy['geometry'].y
    gdf_valid = gdf_copy[[name, 'lon', 'lat']]
    
    # Remove duplicates so we can save time and run kmeans on the unique spatial points
    gdf_sp = gdf_valid.drop_duplicates()
    # We need on the lat and lat for the kmeans to run 
    lon_lat = gdf_sp.copy().drop(columns = name)
    
    for i in range(1, nfolds + 1):
        kmeans = KMeans(n_clusters = i,  random_state = random_state, **kwargs)
        kmeans.fit(lon_lat)

    cluster_labels = kmeans.predict(lon_lat)

    lon_lat['folds'] = cluster_labels + 1
    lon_lat[name] = gdf_sp[name]
    
    lon_lat_valid = lon_lat[[name, 'folds']]
    
    # assign the folds-clusters to the original gdf 
    gdf_kfold_clusters = gdf.merge(lon_lat_valid, on= name, how='left')
    
    return gdf_kfold_clusters
