import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import requests
import numpy as np
import matplotlib.pyplot as plt

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..' , '.env'))

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

def get_google_maps_image(lat, lon, api_key, zoom=18, size='640x640'):
    '''
    Retrieves an image from Google Maps Static API centered on the given coordinates.

    Default zoom for 1km^2 is 18, but best with 17.
    '''
    url = 'https://maps.googleapis.com/maps/api/staticmap'
    params = {
        'center': f'{lat},{lon}',
        'zoom': zoom,
        'size': size,
        'maptype': 'satellite',
        'key': api_key
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        return image
    else:
        print('Error fetching map image from Google Maps API')
        return None

def deegree_to_coords(degrees, minutes, seconds):
    '''
    Converts geographic coordinates to normal coordinates that are uses in google maps api.

    Also rounds to 4 decimal places.
    '''
    return round(degrees + (minutes/60) + (seconds/3600), 4)

def display_image_as_matrix(image):
    '''
    Display images from google maps api as matrix

    If not say 
        Image is None

    '''

    if image is not None:
        # Convert image to a NumPy array
        image_array = np.array(image)
        
        # Print each row of the matrix
        print('Image as Matrix (RGB values):')
        for row in image_array:
            print(row)
    else:
        print('[Warring] Image is None')

def display_image(image):
    '''
        Display image as image
    '''
    plt.imshow(image)
    plt.show()


if __name__ == '__main__':
    latitude = deegree_to_coords(51, 47, 44)
    longitude = deegree_to_coords(19,26,48)
    print(latitude, longitude)
    image = get_google_maps_image(latitude, longitude, GOOGLE_MAPS_API_KEY, zoom=16)
    display_image_as_matrix(image)
    display_image(image)