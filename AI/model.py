import torch
import torch.nn as nn
import torchvision.models as models

class SiameseNetwork(nn.Module):
    def __init__(self):
        super(SiameseNetwork, self).__init__()
        # Feature extractor (shared for both branches)
        backbone = models.resnet18(pretrained=True)
        self.feature_extractor = nn.Sequential(*list(backbone.children())[:-2])  # Remove FC layer and AvgPool
        
        # Bounding box regression head
        self.bbox_head = nn.Sequential(
            nn.Flatten(),
            nn.Linear(224*224, 1024),  # Combine features from both images
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, 4)  # Output: [x_min, y_min, x_max, y_max]
        )
        # Note: This works but there is something off with this. The model is not learning properly.
        # I will need to check the data and the model again. I will also need to check the loss function.

        
    def forward(self, large_image, small_image):
        print(large_image.shape)
        # Extract features from both images
        large_features = self.feature_extractor(large_image)
        small_features = self.feature_extractor(small_image)
        
        print(large_image.shape)
        # Flatten and concatenate features
        combined_features = torch.cat(
            (large_features.view(large_features.size(0), -1),
             small_features.view(small_features.size(0), -1)),
            dim=1
        )
        print(combined_features.shape)
        # Predict bounding box
        bbox = self.bbox_head(combined_features)
        return bbox

        
