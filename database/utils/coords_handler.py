__doc__ = '''
    This file was created to handle coords transformation/calculation
'''
import random
import math
from typing import Tuple

def calc_coords():
    pass

def get_random_coords_in_range():
    pass

def generate_random_coords_for_city(
    max_north: float,
    max_south: float,
    max_east: float,
    max_west: float,
) -> Tuple[float, float]:
    """
    Generate a list of random (lat, lon) within the given bounds.

    Args: 
    max_north, max_south, max_east, max_west - are coords of city in every directory

    Return:
    lat, lon - random point somewhere between those coordinates
    """

    lat = random.uniform(max_south, max_north)
    lon = random.uniform(max_west, max_east)
    
    return lat, lon

import random
from typing import Tuple

def degrees_per_pixel(zoom: int) -> float:
    return 156543.03392 / (2 ** zoom) / 111320

def generate_zoom19_coords_inside_zoom17(
    center_lat: float,
    center_lon: float,
    image_size_px: int = 640,
    zoom_big: int = 17,
    zoom_small: int = 19,
) -> Tuple[float, float]:
    """
    Generate coordinates for zoom19 image that fits completely within zoom17 image.
    
    Args:
        center_lat, center_lon: Center of zoom17 image
        image_size_px: Size of image in pixels (assumes square)
        zoom_big: Zoom level of the big image (default 17)
        zoom_small: Zoom level of the small image (default 19)

    Returns:
        Tuple[float, float]: center_lat, center_lon for zoom19 image
    """

    # Stopniowy rozmiar dużego zdjęcia
    deg_per_pixel_big = degrees_per_pixel(zoom_big)
    deg_per_pixel_small = degrees_per_pixel(zoom_small)

    size_big_deg = image_size_px * deg_per_pixel_big
    size_small_deg = image_size_px * deg_per_pixel_small

    # Granice dużego zdjęcia (zoom17)
    north = center_lat + size_big_deg / 2
    south = center_lat - size_big_deg / 2
    east = center_lon + size_big_deg / 2
    west = center_lon - size_big_deg / 2

    # Możliwy zakres środków dla małego zdjęcia (zoom19),
    # aby jego brzegi nie wychodziły poza duże zdjęcie
    max_lat = north - size_small_deg / 2
    min_lat = south + size_small_deg / 2
    max_lon = east - size_small_deg / 2
    min_lon = west + size_small_deg / 2

    new_lat = random.uniform(min_lat, max_lat)
    new_lon = random.uniform(min_lon, max_lon)

    return new_lat, new_lon


def calculate_random_offset(lat, lon, zoom=17, max_distance=None):
    '''
    Calculate random place inside coords
    '''
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

def coordinates_to_pixels(center_coords, target_coords, img_size=640, resized_size=240):
    """
    Converts geographical coordinates to pixel positions in an image.

    Parameters:
        center_coords (tuple): (latitude, longitude) of the image center.
        target_coords (tuple): (latitude, longitude) of the target point.
        img_size (int): Size of the original square image (default 640x640).
        resized_size (int): Size of the resized square image (default 240x240).

    Returns:
        tuple: Pixel position (x, y) in the resized image.
    """
    # Define the field of view (assumed range in degrees for lat/lon in the image)
    # These values may need tuning based on the zoom level and Google Maps projection.
    lat_range = 0.01  # Approximate latitude span covered by the image
    lon_range = 0.01  # Approximate longitude span covered by the image

    # Calculate degrees per pixel for the original image
    degrees_per_pixel_lat = lat_range / img_size
    degrees_per_pixel_lon = lon_range / img_size

    # Offset the target coordinates relative to the center
    delta_lat = target_coords[0] - center_coords[0]
    delta_lon = target_coords[1] - center_coords[1]

    # Convert offsets to pixel positions in the original image
    pixel_x = img_size / 2 + delta_lon / degrees_per_pixel_lon
    pixel_y = img_size / 2 - delta_lat / degrees_per_pixel_lat

    # Handle resizing: Scale the pixel positions to the resized image
    resize_factor = resized_size / img_size
    resized_pixel_x = pixel_x * resize_factor
    resized_pixel_y = pixel_y * resize_factor

    return int(round(resized_pixel_x)), int(round(resized_pixel_y))