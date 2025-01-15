import torch
from torch.utils.data import DataLoader
from AI.model import SiameseNetwork
from AI.customDataLoader import ImagePairDataset, transform, csv_file, image_dir, l_epochs
import os

def custom_collate_fn(batch):
    # Filter out None samples
    batch = [item for item in batch if item is not None]
    if len(batch) == 0:
        return None
    return torch.utils.data.dataloader.default_collate(batch)

if __name__ == '__main__':
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    model = SiameseNetwork().to(device)
    criterion = torch.nn.MSELoss() # Loss function for bounding box regression that i use
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # Check if the CSV file exists
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file not found: {csv_file}")

    dataset = ImagePairDataset(csv_file, image_dir, transform=transform)

    dataloader = DataLoader(dataset, batch_size=4, shuffle=True, collate_fn=custom_collate_fn)

    # Training 
    epochs = l_epochs
    for epoch in range(epochs):
        model.train()
        loss = 0.0

        # Iterate over data
        for batch in dataloader:
            if batch is None:
                continue  # Skip empty batches
            large_image, small_image, bbox = batch

            large_image = large_image.to(device)
            small_image = small_image.to(device)
            bbox = bbox.to(device)

            optimizer.zero_grad()

            # Forward pass
            prediction = model(large_image, small_image)

            # Calculate loss
            loss = criterion(prediction, bbox)
            loss.backward()
            optimizer.step()

            loss += loss.item()
        print(f'Epoch {epoch+1}/{epochs}, Loss {loss:.4f}')

    torch.save(model.state_dict(), 'AI/models/siamese.pth')
    print('Model saved')