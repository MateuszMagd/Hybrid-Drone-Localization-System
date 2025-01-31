import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import torchvision.transforms as transforms

def displey_two_images(image_one, image_two):
    '''
    Display 2 images
    '''
    fig, axs = plt.subplots(1, 2, figsize=(10,10)) # 1 row 2 col

    axs[0].imshow(image_one)
    axs[1].imshow(image_two)

    plt.show()


def display_image(image):
    '''
    Display image as image
    '''
    if image is None:
        print("[Error] Image is None")
        return 
    plt.imshow(image)
    plt.show()

# Funkcja dodająca czerwoną kropkę na obrazie
def add_red_dot_to_image(image, radius=10):
    '''
    Add big big dot in middle of image
    '''
    # Convert into RGB
    image = image.convert("RGB")
    
    # Now convert to numpy
    image_np = np.array(image)
    
    # Center
    center = (image_np.shape[1] // 2, image_np.shape[0] // 2)
    
    for i in range(center[1] - radius, center[1] + radius):
        for j in range(center[0] - radius, center[0] + radius):
            if (i - center[1])**2 + (j - center[0])**2 <= radius**2:  # Check if point in coords
                # Set Red pixels
                if 0 <= i < image_np.shape[0] and 0 <= j < image_np.shape[1]:
                    image_np[i, j] = [255, 0, 0]
    
    # Convert to PIL
    return Image.fromarray(image_np)

def convert_pil_to_opencv(pil_image):
    """
    Converts a PIL image to an OpenCV-compatible NumPy array in grayscale.
    """
    if pil_image is None:
        raise ValueError("PIL image is None and cannot be converted.")
    
    # Convert PIL to NumPy array
    rgb_array = np.array(pil_image)

    # Check if image is RGB or grayscale
    if len(rgb_array.shape) == 3 and rgb_array.shape[2] == 3:
        # Convert RGB to grayscale
        gray_image = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2GRAY)
    elif len(rgb_array.shape) == 2:
        # Already grayscale
        gray_image = rgb_array
    else:
        raise ValueError("Unexpected image format for conversion.")
    
    return gray_image

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

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])