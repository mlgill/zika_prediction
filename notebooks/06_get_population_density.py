import pandas as pd
import numpy as np
from csv_pkl_sql import csv_it, sql_it
import cPickle as pickle

from osgeo import gdal

# Import the latitude and longitude data
lat_long_data = pd.read_csv('../csv/01_latitude_longitude_google.csv')


# Import the geoTIF map
ds = gdal.Open('../gpw_population_density/gpw-v4-population-density_2015.tif')

rows = ds.RasterYSize
cols = ds.RasterXSize

transform = ds.GetGeoTransform()
xOrigin = transform[0]
yOrigin = transform[3]
pixelWidth = transform[1]
pixelHeight = transform[5]

# My data has one band, otherwise would have to iterate through bands
band = ds.GetRasterBand(1)


def get_population_density(latitude, longitude, 
                           xOrigin=xOrigin, yOrigin=yOrigin,
                           pixelWidth=pixelWidth, pixelHeight=pixelHeight,
                           band=band):

    # # Single point, x=longitude, y=latitude
    # x = -155.662499999999824
    # y = 19.0041666666754416
    x = longitude
    y = latitude

    # This reads three pixels in x- and y- direction
    try:
        # Subtract one off the end because I want to read 3 x 3 region
        size = 100

        dist_matrix = np.meshgrid(np.arange(-size, size+1), 
                                  np.arange(-size, size+1))
        dist_matrix = np.sqrt((dist_matrix[0]**2 + dist_matrix[1]**2))
        sort_order = dist_matrix.ravel().argsort()

        xOffset = int((x - xOrigin) / pixelWidth) - size
        yOffset = int((y - yOrigin) / pixelHeight) - size

        data = band.ReadAsArray(xOffset, yOffset, 2*size+1, 2*size+1)
        data_sort = data.ravel()[sort_order]

        density = data_sort[data_sort>0][:9].mean()
    except:
        density = np.NaN

    return density


lat_long_data['density_per_km'] = lat_long_data.apply(lambda x: get_population_density(x.latitude, x.longitude), axis=1)

#lat_long_data[['location','density_per_km']].to_csv('../csv/06_population_density.csv')
csv_it(lat_long_data[['location','density_per_km']], '06_population_density')

with open('../pkl/06_population_density.pkl', 'w') as fh:
    pickle.dump(lat_long_data[['location','density_per_km']], fh)

sql_it(lat_long_data[['location','density_per_km']], '06_population_density')
