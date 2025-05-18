from typing import List
import matplotlib.pyplot as plt
from collections import defaultdict
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import os
import re
import numpy as np
from pathlib import Path

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

def save_photo(photo: Image, directory: str = "./"):
    '''
    Save photo to a directory or in the same place as function
    '''
    photo.save(directory)

def load_photo(directory: str = None):
    if directory == None:
        print('Wrong directory!')
    
    return Image.open(directory)

def image_similarity(img1, img2):
    img1 = img1.convert('L')  # convert to grayscale
    img2 = img2.convert('L')

    img1 = img1.resize((256, 256))  # resize to match dimensions
    img2 = img2.resize((256, 256))

    arr1 = np.array(img1)
    arr2 = np.array(img2)

    similarity, _ = ssim(arr1, arr2, full=True)
    return similarity

def is_mostly_one_color(image_or_path, threshold=20):
    """
    Checks if the image is mostly one color.
    `threshold` controls tolerance of color variance (lower = stricter).
    
    Args:
      image: PIL Image object (RGB or grayscale)
      threshold: std dev threshold for color variance
      
    Returns:
      True if image is mostly one color (low color variance)
    """
     # Jeśli dostaniesz ścieżkę, otwórz obraz
    if isinstance(image_or_path, str):
        image = Image.open(image_or_path)
    else:
        image = image_or_path

    img = image.convert('RGB')
    arr = np.array(img)
    stddev = arr.std(axis=(0,1))
    return np.all(stddev < threshold)

def get_all_placeholders():
    directory: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\placeholders'
    all_paths = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    placeholders: List = []
    for path in all_paths:
        placeholders.append(load_photo(path))

    return placeholders

def get_all_photo_paths(directory: str = None):
    if directory == None:
        print('Wrong directory!')

    all_paths = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    pattern = re.compile(r'^(.*)_zoom(17|19)\.png$')
    groups = defaultdict(dict)

    for path in all_paths:
        filename = os.path.basename(path)
        match = pattern.match(filename)
        if match:
            prefix, zoom = match.groups()
            groups[prefix][zoom] = path

    paired_paths = []
    for zoom_dict in groups.values():
        if '17' in zoom_dict and '19' in zoom_dict:
            paired_paths.append([zoom_dict['17'], zoom_dict['19']])

    return paired_paths

def save_ready_to_label(photo_directory: str = './' , save_directory: str = './') -> bool:
    '''
    Function to copy photo from one directory to other

    Args:
    photo_directory - directory to photo 
    save_directory - new directory where photo should be saved

    Return:
    bool - If operation was sucessful return True, else False
    
    '''
    
    try:
        photo_path = Path(photo_directory.replace("\\", "/"))
        save_dir = Path(save_directory)

        photo = Image.open(photo_path)
        photo.save(save_dir / photo_path.name)
    except Exception as e:
        print(f"Error! : {e}")
        return False
        
    return True

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

