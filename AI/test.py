import torch
from PIL import Image
from AI.customDataLoader import transform, large_image_path, small_image_path
from AI.model import SiameseNetwork
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def predict_small_image_location(model, large_image_path, small_image_path, transform):
    model.eval()
    
    # Load and preprocess images
    large_image = Image.open(large_image_path).convert("RGB")
    small_image = Image.open(small_image_path).convert("RGB")
    large_image = transform(large_image).unsqueeze(0).to(device)
    small_image = transform(small_image).unsqueeze(0).to(device)
    
    # Predict bounding box
    with torch.no_grad():
        bbox = model(large_image, small_image)
    
    return bbox.cpu().numpy()

# Function to visualize the results
def visualize_results(large_image_path, small_image_path, bbox):
    print(bbox)
    # Load images
    large_image = Image.open(large_image_path).convert("RGB")
    small_image = Image.open(small_image_path).convert("RGB")

    # Create a figure with 3 subplots
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    
    # Plot large image
    axs[0].imshow(large_image)
    axs[0].set_title("Large Image (Zoom17)")
    axs[0].axis("off")
    
    # Plot small image
    axs[1].imshow(small_image)
    axs[1].set_title("Small Image (Zoom19)")
    axs[1].axis("off")
    
    # Plot large image with bounding box
    axs[2].imshow(large_image)
    axs[2].set_title("Prediction (Zoom17 + Box)")
    axs[2].axis("off")
    
    # Draw the predicted bounding box on the large image
    bbox = bbox[0]  # Assuming bbox is [[x_min, y_min, x_max, y_max]]
    x_min, y_min, x_max, y_max = bbox
    
    size = 100

    # Add bounding box as a rectangle
    rect = patches.Rectangle(
        (x_min, y_min),   # Coordinates
        size,       # Width
        size,       # Height
        linewidth=2, edgecolor="red", facecolor="none"
    )

    # Add bounding box as a rectangle
    rect_max = patches.Rectangle(
        (x_max, y_max),   # Coordinates
        size,       # Width
        size,       # Height
        linewidth=2, edgecolor="blue", facecolor="none"
    )

    print(rect)
    print(rect_max)
    axs[2].add_patch(rect)
    axs[2].add_patch(rect_max)

    # Show the plot
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # Load the model
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    model = SiameseNetwork().to(device)

    # Load trained weights
    model.load_state_dict(torch.load("AI/models/siamese.pth", map_location=device))
    model.eval()

    bbox = predict_small_image_location(model, large_image_path, small_image_path, transform)
    print("Predicted bounding box:", bbox)
    # Visualize the results
    visualize_results(large_image_path, small_image_path, bbox)
