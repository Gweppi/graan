import fiona
import rasterio
import rasterio.mask

with fiona.open("shape.shp", "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

    with rasterio.open("name.tif") as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta