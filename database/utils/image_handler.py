import matplotlib.pyplot as plt
import pandas
import numpy as np

def display_image(image):
    '''
    Display image as image
    '''
    if image is None:
        print("[Error] Image is None")
        return 
    plt.imshow(image)
    plt.show()

def displey_two_images(image_one, image_two):
    '''
    Display 2 images
    '''
    fig, axs = plt.subplots(1, 2, figsize=(10,10)) # 1 row 2 col

    axs[0].imshow(image_one)
    axs[1].imshow(image_two)

    plt.show()

def save_photo(photo, directory = "./"):
    '''
    Save photo to a directory or in the same place as function
    '''

    photo.to_csv('G:/project/Thesis/Database/coordinates.csv', index=False)

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

