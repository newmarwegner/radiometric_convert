import sys
import rasterio
import os
from pathlib import Path
from rasterio.merge import merge


def create_destination_folder():
    dir=os.getcwd()+'/images/rebuild'
    if not os.path.exists(dir):
        os.makedirs(dir)
    else:
        pass
    return

def list_images():
    rasters_paths = []
    for root, directory, files in os.walk(os.getcwd()+'/images'):
        for filename in files:
            if filename.endswith('.tif') and not '_CONVERTED' in filename:
                rasters_paths.append(os.getcwd()+f'/images/{filename}')

    return rasters_paths

def convert_radiometric(raster_paths,bits):
    if bits == 8:
        type = rasterio.uint8
    else:
        type = rasterio.uint16

    for raster in raster_paths:
        filename = (Path(raster).name).rsplit('.',1)[0]
        src = rasterio.open(raster)
        mosaic, out_trans = merge([src,])
        out_meta = src.meta.copy()
        out_meta.update({"driver": "GTiff",
                 "dtype": type,
                 "height": mosaic.shape[1],
                 "width": mosaic.shape[2],
                 "transform": out_trans,
                 "crs": src.crs
                 }
                )
        with rasterio.open(f'{os.getcwd()}/images/rebuild/{filename}_CONVERTED_{bits}bits.tif',
                           "w",
                           **out_meta) as dest:
            dest.write(mosaic.astype(type))

    return

def main():
    create_destination_folder()
    raster_paths=list_images()
    convert_radiometric(raster_paths,bits)

    return

if __name__ == '__main__':
    args = sys.argv
    bits = int(args[1])
    main()


