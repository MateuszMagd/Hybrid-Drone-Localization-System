import torch
from torch.utils.data import Dataset
import torchvision.transforms as transforms
import pandas as pd
from PIL import Image
import os

class ImagePairDataset(Dataset):
    def __init__(self, csv_file, image_folder, transform=None):
        self.data = pd.read_csv(csv_file)
        self.image_folder = image_folder
        self.transform = transform
        self.image_size = 640  # Assuming 640x640 pixels for both images

    def __getitem__(self, idx):
        row = self.data.iloc[idx]

        try:
            # Load image paths
            large_image_path = os.path.join(self.image_folder, f"{row['CityName']}_{row['index']}_zoom17.png")
            small_image_path = os.path.join(self.image_folder, f"{row['CityName']}_{row['index']}_zoom19.png")

            # Calculate normalized bounding box coordinates
            x_center = (row['NewLongitude'] - row['RandomLongitude']) / 0.05 + 0.5
            y_center = (row['NewLatitude'] - row['RandomLatitude']) / 0.05 + 0.5
            box_size = 0.1  # Assuming small image is 10% of the large image in width/height
            x_min = x_center - box_size / 2
            y_min = y_center - box_size / 2
            x_max = x_center + box_size / 2
            y_max = y_center + box_size / 2

            bbox = torch.tensor([x_min, y_min, x_max, y_max], dtype=torch.float32)

            # Load and preprocess images
            large_image = Image.open(large_image_path).convert("RGB")
            small_image = Image.open(small_image_path).convert("RGB")

            if self.transform:
                large_image = self.transform(large_image)
                small_image = self.transform(small_image)

            # Return large image, small image, and bounding box
            return large_image, small_image, bbox

        except Exception as e:
            # Log error and skip this sample
            print(f"Error loading image paths or processing row {idx}: {e}")
            return None

    def __len__(self):
        return len(self.data)
    
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

current_path = os.getcwd()
print("Current Path:", current_path)

csv_file = 'Database/sample_coords.csv'
image_dir = 'Database/photos'

# Example usage
large_image_path = "Database/photos/Chicago_20_zoom17.png"
small_image_path = "Database/photos/Chicago_20_zoom19.png"