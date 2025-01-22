from autonomous_arena.data_handler import create_dataset, AutonomousDataset
from autonomous_arena.training_pipeline import train_model, evaluate_model
import torch
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim


def fine_tuning(model, path_2_custom_ds):
    train_images, test_images, train_labels, test_labels = create_dataset(path_2_custom_ds)
    train_dataset = AutonomousDataset(train_images, train_labels)
    test_dataset = AutonomousDataset(test_images, test_labels)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    num_classes = train_labels.shape[1]
    model.fc2 = nn.Linear(model.fc2.in_features, num_classes)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    epochs = 10
    train_model(model, train_loader, criterion, optimizer, device, epochs)

    evaluate_model(model, test_loader, device)

    return model


