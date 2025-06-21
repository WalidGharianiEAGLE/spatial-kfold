import geopandas as gpd
import pkg_resources


def load_ames():
    # Load ames.geojson file
    filepath = pkg_resources.resource_filename(__name__, "data/ames.geojson")
    data = gpd.read_file(filepath)

    return data
