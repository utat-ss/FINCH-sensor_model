import rasterio
from rasterio.io import MemoryFile
from rasterio.transform import from_gcps
from rasterio.control import GroundControlPoint
import os
import math
import geopandas as gpd
from rasterio import features

# Define your GCPs as a list of GroundControlPoints
# Example format: [(pixel_x, pixel_y, lng, lat)]
gcps = [
    GroundControlPoint(0, 0, -68.1620, -19.3610),  # Top-left corner
    GroundControlPoint(400, 0, -68.1500, -19.3610),  # Top-right corner
    GroundControlPoint(400, 400, -68.1500, -19.3700),  # Bottom-right corner
    GroundControlPoint(0, 400, -68.1620, -19.3700)  # Bottom-left corner
]

def getGeoTiffWithGCPs(png_path, output_path, gcps):
    dataset = rasterio.open(png_path)
    bands = [1]
    data = dataset.read(bands)
    
    # Create a transform based on GCPs
    transform = from_gcps(gcps)
    
    crs = rasterio.crs.CRS({"init": "epsg:4326"})
    
    with rasterio.open(os.path.join(output_path, "salt_flat_with_gcps.tiff"), 'w', driver='GTiff',
                    width=data.shape[1], height=data.shape[2],
                    count=3, dtype=data.dtype, nodata=0,
                    transform=transform, crs=crs, gcps=gcps) as dst:
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
