

import torch


def test():
    try:
        # Load image paths
        large_image_path = os.path.join(self.image_folder, f"{row['CityName']}_{row['index']}_zoom17.png")
        small_image_path = os.path.join(self.image_folder, f"{row['CityName']}_{row['index']}_zoom19.png")

        new_longitude_pixel, new_latitude_pixel = coordinates_to_pixels((row['RandomLongitude'], row['RandomLatitude']), (row['NewLongitude'], row['NewLatitude']))
            
        # Calculate bounding box 
        x_center = new_longitude_pixel
        y_center = new_latitude_pixel
        box_size = 0.1  # Assuming small image is 10% of the large image in width/height
        x_min = x_center - box_size / 2
        y_min = y_center - box_size / 2
        x_max = x_center + box_size / 2
        y_max = y_center + box_size / 2
        bbox = torch.tensor([x_min, y_min, x_max, y_max], dtype=torch.float32)

        # Return large image, small image, and bounding box
        return large_image, small_image, bbox

    except Exception as e:
        # Log error and skip this sample
        print(f"Error loading image paths or processing row {idx}: {e}")
        return None