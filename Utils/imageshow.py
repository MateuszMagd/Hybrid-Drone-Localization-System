import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

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