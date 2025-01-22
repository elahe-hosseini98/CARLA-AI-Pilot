from data_handler import create_dataset, AutonomousDataset
from training_pipeline import SimpleCNN, train_model, evaluate_model
import torch
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim


if __name__ == "__main__":
    path_2_dataset = "autonomous_arena.csv"
    train_images, test_images, train_labels_encoded, test_labels_encoded = create_dataset(path_2_dataset)

    train_dataset = AutonomousDataset(train_images, train_labels_encoded)
    test_dataset = AutonomousDataset(test_images, test_labels_encoded)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    num_classes = train_labels_encoded.shape[1]
    model = SimpleCNN(num_classes).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    epochs = 20

    train_model(model, train_loader, criterion, optimizer, device, epochs)
    evaluate_model(model, test_loader, device)

    try:
        torch.save(model.state_dict(), "autonomous_arena_pretrained_model.pth")
        print("Model was successfully saved as 'autonomous_arena_pretrained_model.pth'")
    except:
        print("An error happened while saving the model!")
