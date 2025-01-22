import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import torch
from torch.utils.data import Dataset


class AutonomousDataset(Dataset):
    def __init__(self, images, labels):
        self.images = torch.tensor(images)
        self.labels = torch.tensor(labels)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.images[idx], self.labels[idx]


def create_dataset(path_2_dataset):
    trackData = pd.read_csv(path_2_dataset)
    labels = trackData["448"].values
    images = trackData.drop("448", axis=1).values  # Images

    images = images / 255.0
    images = images.reshape(-1, 1, 14, 32).astype(np.float32)

    train_images, test_images, train_labels, test_labels = train_test_split(
        images, labels, test_size=0.3, random_state=42
    )

    one_hot_encoder = OneHotEncoder(sparse_output=False)
    train_labels_encoded = one_hot_encoder.fit_transform(train_labels.reshape(-1, 1))
    test_labels_encoded = one_hot_encoder.transform(test_labels.reshape(-1, 1))

    '''
    Left -> [0. 1. 0. 0.] = 1
    Forward -> [1. 0. 0. 0.] = 0
    Right -> [0. 0. 1. 0.] = 2
    Stop -> [0. 0. 0. 1.] = 3
    '''

    return train_images, test_images, train_labels_encoded, test_labels_encoded