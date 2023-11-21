import numpy as np
from torch.utils.data import Dataset


class ResNetDataset(Dataset):
  
    def __init__(self, images, labels, transform):
        self.images = images
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):

        image = self.transform(self.images[idx])
        label = np.squeeze(self.labels[idx])
                
        return image, label
    