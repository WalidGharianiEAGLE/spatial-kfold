from typing import Union
import math

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import box
from shapely.geometry import Polygon


def create_grid(
    gdf: gpd.GeoDataFrame,
    width: Union[int, float],
    height: Union[int, float],
    grid_type="rect",
) -> gpd.GeoDataFrame:
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
    grid_type : str
        Either 'rect' for rectangular grid or 'hex' for hexagonal grid.

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
    if grid_type not in ["rect", "hex"]:
        raise ValueError(
            f"Invalid grid_type {grid_type}. Specify either 'rect' or 'hex'."
        )
    if grid_type == "rect":
        if not (isinstance(height, (int, float)) and height > 0):
            raise ValueError("Height must be a positive number for 'rect' grid.")

    # Get the bounds of the points
    xmin, ymin, xmax, ymax = gdf.total_bounds
    polygons = []

    if grid_type == "rect":
        cols = np.arange(xmin, xmax + width, width)
        rows = np.arange(ymin, ymax + height, height)
        polygons = [
            box(x, y, x + width, y + height) for x in cols[:-1] for y in rows[:-1]
        ]

    elif grid_type == "hex":
        sqrt3 = np.sqrt(3)
        cos = sqrt3 / 2  # cos(30°)
        r = width / 2  # center to flat
        R = r / cos  # circumradius (center to corner)
        dx = 3 / 2 * R  # horizontal distance between centers
        dy = sqrt3 * R  # vertical distance between rows

        x = xmin
        col = 0
        while x < xmax + dx:
            y_offset = 0 if col % 2 == 0 else dy / 2
            y = ymin + y_offset
            while y < ymax + dy:
                polygons.append(_create_flat_top_hexagon(x, y, R))
                y += dy
            x += dx
            col += 1

    return gpd.GeoDataFrame({"geometry": polygons}, crs=gdf.crs)


def _create_flat_top_hexagon(cx: float, cy: float, R: float) -> Polygon:
    """
    Create a flat-topped hexagon centered at (cx, cy) with circumradius R.
    """
    return Polygon(
        [
            (
                cx + R * math.cos(math.radians(angle)),
                cy + R * math.sin(math.radians(angle)),
            )
            for angle in [0, 60, 120, 180, 240, 300]
        ]
    )


def spatial_blocks(
    gdf: gpd.GeoDataFrame,
    width: Union[int, float],
    height: Union[int, float],
    nfolds: int,
    method="random",
    orientation="tb-lr",
    grid_type: str = "rect",
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
    grid_type : str
        'rect' or 'hex'.
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
    if method not in ["random", "continuous"]:
        raise ValueError(
            f"Invalid method {method}. Specify either 'random' or 'continuous'."
        )
    elif orientation not in ["tb-lr", "bt-rl"]:
        raise ValueError(
            f"Invalid orientation {orientation}. Specify either 'tb-lr' or 'bt-rl'. By default the orientation is 'tb-lr'."
        )

    # Create GeoDataFrame containing the grid of polygons
    grids = create_grid(gdf, width, height, grid_type)

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
    block_indices = np.array_split(sp_blocks.index, nfolds)
    blocks_list = [sp_blocks.loc[idx].assign(folds=i) for i, idx in enumerate(block_indices, start=1)]

    # Set as Create a geodataframe
    blocks_folds_gdf = gpd.GeoDataFrame(pd.concat(blocks_list))

    return blocks_folds_gdf
