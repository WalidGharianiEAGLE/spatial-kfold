import geopandas as gpd
from sklearn.cluster import KMeans
from sklearn.cluster import BisectingKMeans


def spatial_kfold_clusters(
    gdf: gpd.GeoDataFrame,
    name: str,
    nfolds: int,
    algorithm="kmeans",
    random_state=None,
    **kwargs
):
    """
    Perform spatial clustering using KMeans or BisectingKMeans on a GeoDataFrame with coordinates
    and assign each geo point to a fold.

    Parameters
    ----------
    gdf : GeoDataFrame
        The GeoDataFrame with a geometry column containing the points to use for spatial clustering.
    name : str
        Name of the column that identifies each unique geospatial point (e.g., station_id or city_code).
    nfolds : int
        The number of clusters/folds to assign for each geospatial point.
    algorithm : str, optional
        The clustering algorithm to use ('kmeans' or 'bisectingkmeans'). Default is 'kmeans'.
    kwargs : set of arguments to provide for each algorithm:
        - For kmeans from sklearn API:
        https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
        e.g., algorithm {"lloyd", "elkan", “auto”, “full”}, default=”lloyd”
        - For bisectingkmeans from sklearn API:
        https://scikit-learn.org/stable/modules/generated/sklearn.cluster.BisectingKMeans.html
        e.g.,{“lloyd”, “elkan”}, default=”lloyd”
    random_state : int, optional
        An optional integer seed to use for centroid initialization.

    Returns
    -------
    GeoDataFrame
        A GeoDataFrame containing a 'folds' column.
    """
    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("Input must be a GeoDataFrame.")
    if gdf.crs == None:
        raise AttributeError(
            "The passed GeoDataFrame has no CRS. Use `to_crs()` to reproject one of the input geometries."
        )
    if not (isinstance(nfolds, int) and nfolds > 0):
        raise ValueError("nfolds must be a positive int number.")
    if algorithm not in ["kmeans", "bisectingkmeans"]:
        raise ValueError(
            'Unsupported clustering algorithm. Use "kmeans" or "bisectingkmeans".'
        )

    gdf_copy = gdf.reset_index().copy().drop(columns=["index"])
    gdf_copy["lon"] = gdf_copy["geometry"].centroid.x
    gdf_copy["lat"] = gdf_copy["geometry"].centroid.y
    gdf_valid = gdf_copy[[name, "lon", "lat"]]

    # Remove duplicates so we can save time and run the algorithm on the unique spatial points
    gdf_sp = gdf_valid.drop_duplicates()
    # We need only the 'lat' and 'lat' for the algorithm to run
    lon_lat = gdf_sp.copy().drop(columns=name)

    if algorithm == "kmeans":
        clustering_model = KMeans(
            n_clusters=nfolds, random_state=random_state, **kwargs
        )
    elif algorithm == "bisectingkmeans":
        clustering_model = BisectingKMeans(
            n_clusters=nfolds, random_state=random_state, **kwargs
        )
    clustering_model.fit(lon_lat)
    cluster_labels = clustering_model.predict(lon_lat)

    lon_lat["folds"] = cluster_labels + 1
    lon_lat[name] = gdf_sp[name]
    lon_lat_valid = lon_lat[[name, "folds"]]
    # Assign the folds-clusters to the original gdf
    gdf_kfold_clusters = gdf.merge(lon_lat_valid, on=name, how="left")

    return gdf_kfold_clusters
