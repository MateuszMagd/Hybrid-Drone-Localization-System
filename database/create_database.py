__doc__ = '''
    This file is to create and eliminate photos that are not good for model AI.
'''

import pandas as pd

from get_data_from_api import get_google_maps_image
from utils.coords_handler import generate_random_coords_for_city
from utils.image_handler import save_photo

# CONST VAR FOR THIS FILE
PHOTOS = 5 # Photo for each region
BIG_ZOOM = 17 # Zoom for large photo
SMALL_ZOOM = 19 # Zoom for small photo

CITY_DATA_CSV = './database/BasicCityCoords.csv'

def main() -> None:
    '''
    Main function to create database with Google APi.
    '''
    
    city_data = pd.read_csv(CITY_DATA_CSV)

    # TODO: Add if no loaded for city_data

    # Loop for photo creation
    for index, data in city_data.iterrows():
        # General Data
        city_name = data.CityName
        latitude = data.Latitude
        longitude = data.Longitude

        # Max coordination in every way
        max_north = data.MaxNorth
        max_east = data.MaxEast
        max_west = data.MaxWest
        max_south = data.MaxSouth

        print(city_name, latitude, longitude)
        for number_photo in range(PHOTOS):
            big_photo = f"G:/project/Thesis/Database/photos/{city_name}_{number_photo}_zoom17.png"
            small_photo = f"G:/project/Thesis/Database/photos/{city_name}_{number_photo}_zoom19.png"

            lat, lon = generate_random_coords_for_city(max_north, max_south, max_east, max_west)

            zoom19_photo = get_google_maps_image(lat, lon, zoom=19)
            zoom17_photo = get_google_maps_image(lat, lon, zoom=17)

            save_photo(zoom19_photo)
            save_photo(zoom17_photo, )



    


if __name__ == '__main__':
    main()