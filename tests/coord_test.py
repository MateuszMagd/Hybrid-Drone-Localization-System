import numpy as np

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

if __name__ == '__main__':
    # Example usage
    center_coords = (51.5074, -0.1278)  # Example: Center coordinates (lat, lon)
    target_coords = (51.5075, -0.1279)  # Example: Target coordinates (lat, lon)

    pixel_position = coordinates_to_pixels(center_coords, target_coords)
    print("Target pixel position in resized image:", pixel_position)

    pixel_position = coordinates_to_pixels(center_coords, center_coords, resized_size=640)
    print("Target pixel position in resized image:", pixel_position)
