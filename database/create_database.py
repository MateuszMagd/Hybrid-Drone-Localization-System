__doc__ = '''
    This file is to create and eliminate photos that are not good for model AI.
'''

import pandas as pd
from pathlib import Path
import csv

from utils.get_data_from_api import get_google_maps_image
from utils.coords_handler import generate_random_coords_for_city, generate_zoom19_coords_inside_zoom17
from utils.image_handler import save_photo

# CONST VAR FOR THIS FILE
PHOTOS = 5 # Photo for each region
BIG_ZOOM = 17 # Zoom for large photo
SMALL_ZOOM = 19 # Zoom for small photo

CITY_DATA_CSV = './database/BasicCityCoords.csv'
CURRENT_DIFF = Path(__file__).resolve().parent / 'raw_photos'

def main() -> None:
    '''
    Main function to create database with Google APi.
    '''
    
    ##                                        ##
    #----------CREATING AND SAVING-------------#
    ##                                        ##
    # TODO: Add if no loaded for city_data
    city_data = pd.read_csv(CITY_DATA_CSV)

    
    photos_data = [['city', 'index', 'latitude', 'longitude', 'zoom']]
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

        for number_photo in range(PHOTOS):
            big_photo_path = CURRENT_DIFF / f"{city_name}_{number_photo}_zoom17.png"
            small_photo_path = CURRENT_DIFF / f"{city_name}_{number_photo}_zoom19.png"

            lat, lon = generate_random_coords_for_city(max_north, max_south, max_east, max_west)
            
            # TODO: MAKE SMALLER PHOTO REANDOM COORDS INSIDE BIG! ~ DONE
            zoom17_photo = get_google_maps_image(lat, lon, zoom=17)

            # Współrzędne dla zoom19, które zmieszczą się w zoom17
            small_lat, small_lon = generate_zoom19_coords_inside_zoom17(
                center_lat=lat,
                center_lon=lon
            )
            zoom19_photo = get_google_maps_image(small_lat, small_lon, zoom=19)

            save_photo(zoom17_photo, big_photo_path)
            save_photo(zoom19_photo, small_photo_path)
            photos_data.append([city_name, number_photo, lat, lon, '17'])
            photos_data.append([city_name, number_photo, small_lat, small_lon, '19'])
            break
        if index == 5:
            break
    
    # SAVE CSV
    with open('./database/RawPhotoData.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(photos_data)
    


if __name__ == '__main__':
    main()