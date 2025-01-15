from GPSMapGetter.gps import get_google_maps_image
from Utils.imageoperations import displey_two_images, add_red_dot_to_image
import pandas
import random
import math

'''
latitude = 51.7500000  # Szerokość geograficzna
longitude = 19.4666700  # Długość geograficzna

# Pobieramy obrazki z Google Maps
image = get_google_maps_image(lat=latitude, lon=longitude, zoom=16)
image2 = get_google_maps_image(lat=latitude, lon=longitude, zoom=18)

# Dodajemy większą czerwoną kropkę na środku
image_with_dot = add_red_dot_to_image(image, radius=20)
image2_with_dot = add_red_dot_to_image(image2, radius=20)

displey_two_images(image_with_dot, image2_with_dot)

#print(x['MaxTop'])
#val = x['MaxTop'].values[0]
#print(val + 1)

'''

def calculate_random_offset(lat, lon, zoom=17, max_distance=None):
    if max_distance == None:
        max_distance = (500/2) # 500x500 so from center we divide 2 and substract 50 so it fit into bigger image

    # 1 deggre its 111km
    degree_to_meter = 111000
    
    # Max offset
    max_lat_offset = max_distance / degree_to_meter  
    max_lon_offset = max_distance / (degree_to_meter * math.cos(math.radians(lat)))
    
    # Reandom direction
    lat_offset = random.uniform(-max_lat_offset, max_lat_offset)  # Lat
    lon_offset = random.uniform(-max_lon_offset, max_lon_offset)  # Long


    # New coords
    new_lat = lat + lat_offset
    new_lon = lon + lon_offset

    return new_lat, new_lon

if __name__ == '__main__':

    csv_data = pandas.read_csv('coords.csv')

    # Współrzędne początkowe dla zoomu 17
    latitude = 51.7500000  # Szerokość geograficzna
    longitude = 19.4666700  # Długość geograficzna

    coordinates_list = []

    i = 0

    for row in csv_data.itertuples():
        for i in range(100):
            city_name = row.CityName
            latitude = row.Latitude
            longitude = row.Longitude

            # Max Coords
            max_north = row.MaxNorth
            max_east = row.MaxEast
            max_west = row.MaxWest
            max_south = row.MaxSouth

            # Generate random lati and long bettwen coords
            random_latitude = random.uniform(max_south, max_north)  # Between max_south and max_north
            random_longitude = random.uniform(max_west, max_east)  # Between max_west and max_east


            image = get_google_maps_image(lat=random_latitude, lon=random_longitude, zoom=17)

            # Save the image for zoom 17
            image_path = f"G:/project/Thesis/Database/photos/{city_name}_{i}_zoom17.png"
            image.save(image_path)

            # Oblicz nowe współrzędne dla zoomu 19 (mniejszy obszar)
            new_lat, new_lon = calculate_random_offset(random_latitude, random_longitude)
            image2 = get_google_maps_image(lat=new_lat, lon=new_lon, zoom=19)

            # Save the image for zoom 19
            image2_path = f"G:/project/Thesis/Database/photos/{city_name}_{i}_zoom19.png"
            image2.save(image2_path)

            image_with_dot = add_red_dot_to_image(image, radius=20)
            image2_with_dot = add_red_dot_to_image(image2, radius=20)

            #displey_two_images(image_with_dot, image2_with_dot)

            # Save the coordinates for the current city in the list
            coordinates_list.append({
                "CityName": city_name,
                "RandomLatitude": random_latitude,
                "RandomLongitude": random_longitude,
                "index": i,
                "NewLatitude": new_lat,
                "NewLongitude": new_lon
            })

    # Save coordinates to a CSV file
    coordinates_df = pandas.DataFrame(coordinates_list)
    coordinates_df.to_csv('G:/project/Thesis/Database/coordinates.csv', index=False)

