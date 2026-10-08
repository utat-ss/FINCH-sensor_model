import rasterio
from rasterio.io import MemoryFile
from rasterio.transform import from_gcps
from rasterio.control import GroundControlPoint
import os
import math
import geopandas as gpd
from rasterio import features

# Define your GCPs as a list of GroundControlPoints
# Example format: [(pixel_row, pixel_col, lng, lat)]
gcps = [
    GroundControlPoint(295, 207, -68.315237, -19.328803),
    GroundControlPoint(362, 142, -68.404134, -19.416549),
    GroundControlPoint(160, 316, -68.167262, -19.159137),
    GroundControlPoint(625, 234, -68.278207, -19.756831),
    GroundControlPoint(146, 130, -68.421179, -19.136172),
    GroundControlPoint(262, 268, -68.231269, -19.286650)
]

def getGeoTiffWithGCPs(png_path, output_path, gcps):
    dataset = rasterio.open(png_path)
    bands = [1, 2, 3]
    data = dataset.read(bands)
    
    # Create a transform based on GCPs
    transform = from_gcps(gcps)
    
    crs = rasterio.crs.CRS({"init": "epsg:4326"})
    
    with rasterio.open(os.path.join(output_path, "salt_flat_with_gcps.tiff"), 'w', driver='GTiff',
                    width=data.shape[1], height=data.shape[2],
                    count=3, dtype=data.dtype, nodata=0,
                    transform=transform, crs=crs) as dst:
        dst.write(data, indexes=bands)

def getGeojsonWithGCPs(gcps):
    dataset = rasterio.open('testdata.png')
    bands = [1]
    data = dataset.read(bands)

    # Apply GCP-based transform
    transform = from_gcps(gcps)

    crs = rasterio.crs.CRS({"init": "epsg:4326"})

    with MemoryFile() as memfile:
        meta = {"count": 1, "width": data.shape[1], "height": data.shape[2], "transform": transform, "nodata": 0, "crs": crs, "dtype":data.dtype}
        with memfile.open(driver='GTiff', **meta) as dataset:
            dataset.write(data)
            band = dataset.read()
            mask = band != 0

    shapes = features.shapes(band, mask=mask, transform=transform)
    fc = ({"geometry": shape, "properties": {"value": value}} for shape, value in shapes)
    gdf = gpd.GeoDataFrame.from_features(fc)
    gdf.crs = "epsg:4326"

    return gdf

# Call the functions
getGeoTiffWithGCPs('testdata.png', 'output', gcps)
gdf = getGeojsonWithGCPs(gcps)
gdf.to_file(os.path.join('output', f'salt_flat_with_gcps.geojson'), driver='GeoJSON')
