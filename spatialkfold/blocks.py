from typing import Union

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import box


def create_grid(
    gdf: gpd.GeoDataFrame, width: Union[int, float], height: Union[int, float]
):
    """
    Create a grid of polygons with a specified width and height based on the bounds of a provided GeoDataFrame.

    Parameters
    ----------
    gdf : GeoDataFrame
        The GeoDataFrame containing the bounds to use for creating the grid.
    width : int or float
        The width of the grid cells in the x-dimension.
    height : int or float
        The height of the grid cells in the y-dimension.

    Returns
    -------
    GeoDataFrame
        A GeoDataFrame containing the grid polygons.
        Each polygon represents a grid cell with the specified 'width' and 'height'.

    Source: Code for creating a grid was adapted from the solution provided by user "Mativane" in the following
    gis.stackexchange thread: https://gis.stackexchange.com/questions/269243/creating-polygon-grid-using-geopandas
    """
    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("Input must be a GeoDataFrame")
    if gdf.crs == None:
        raise AttributeError(
            "The passed GeoDataFrame has no CRS. Use `to_crs()` to reproject one of the input geometries."
        )
    if not (isinstance(width, (int, float)) and width > 0):
        raise ValueError("Width must be a positive number")
    if not (isinstance(height, (int, float)) and height > 0):
        raise ValueError("Height must be a positive number")

    # Get the bounds of the points
    xmin, ymin, xmax, ymax = gdf.total_bounds

    # Calculate the number of rows and columns in the grid
    cols = list(np.arange(xmin, xmax + width, width))
    rows = list(np.arange(ymin, ymax + height, height))

    # Create the grid polygons
    polygons = [box(x, y, x + width, y + height) for x in cols[:-1] for y in rows[:-1]]
    # Create a geodataframe with the grid polygons and add crs
    grid = gpd.GeoDataFrame({"geometry": polygons})
    grid = grid.set_crs(gdf.crs)

    return grid


def spatial_blocks(
    gdf: gpd.GeoDataFrame,
    width: Union[int, float],
    height: Union[int, float],
    nfolds: int,
    method="random",
    orientation="tb-lr",
    random_state=None,
):
    """
    Create a grid of polygons based on the intersection with a provided GeoDataFrame and assign each polygon
    to a number of fold.

    Parameters
    ----------
    gdf : GeoDataFrame
        The GeoDataFrame containing the points to use for creating the blocks.
    width : int or float
        The width of the grid cells in the x-dimension.
    height : int or float
        The height of the grid cells in the y-dimension.
    nfolds : int
        The number of folds to assign for each polygon.
    method : str, optional
        The method to use for assigning folds to the blocks. Valid values are 'continuous' and 'random'.
        Default is 'random'.
    orientation : str, optional
        The orientation of the grid-folds. Can be 'tb-lr' (top-bottom, left-right) and 'bt-rl' (bottom-top, right-left).
        Default is 'tb-lr'.
    random_state : int, optional
        An optional integer seed to use when shuffling the grid cells. If provided, this allows the shuffling of the grid
        cells to be reproducible.

    Returns
    -------
    GeoDataFrame
        A GeoDataFrame containing the blocks, with a 'folds' column indicating the block number for each polygon.
    """
    if not (isinstance(nfolds, int) and nfolds > 0):
        raise ValueError("nfolds must be a positive int number.")
    if method != "random" and method != "continuous":
        raise ValueError(
            f"Invalid method {method}. Specify either 'random' or 'continuous'."
        )
    elif orientation != "tb-lr" and orientation != "bt-rl":
        raise ValueError(
            f"Invalid orientation {orientation}. Specify either 'tb-lr' or 'bt-rl'. By default the orientation is 'tb-lr'."
        )

    # Create GeoDataFrame containing the grid of polygons
    grids = create_grid(gdf, width, height)

    in_grids = grids.sjoin(gdf, how="inner").drop_duplicates("geometry")
    # Keep only geometry column
    valid_grids = in_grids.copy()[["geometry"]]
    # Reset index and remove index column
    valid_grids = valid_grids.reset_index().copy().drop(columns=["index"])
    # Shuffle the blocks if method = random
    if method == "random":
        sp_blocks = valid_grids.sample(frac=1, random_state=random_state)
    elif method == "continuous" and orientation == "tb-lr":
        sp_blocks = valid_grids
    elif method == "continuous" and orientation == "bt-rl":
        reversed_blocks = valid_grids[::-1].reset_index(drop=True)
        sp_blocks = reversed_blocks

    # Split the data into a certain number of blocks
    split_blocks = np.array_split(sp_blocks, nfolds)
    blocks_list = [arr.assign(folds=i) for i, arr in enumerate(split_blocks, start=1)]

    # Set as Create a geodataframe
    blocks_folds_gdf = gpd.GeoDataFrame(pd.concat(blocks_list))

    return blocks_folds_gdf
