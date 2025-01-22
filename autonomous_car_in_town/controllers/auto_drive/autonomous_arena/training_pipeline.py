from sklearn.metrics import confusion_matrix
import torch.nn as nn
import numpy as np
import torch


class SimpleCNN(nn.Module):
    def __init__(self, num_classes):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(32 * 7 * 16, 128)
        self.fc2 = nn.Linear(128, num_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)  # Flatten the tensor
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x


def train_model(model, train_loader, criterion, optimizer, device, epochs):
    model.train()
    for epoch in range(epochs):  # Number of epochs
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            # Collect accuracy metrics
            _, predicted = torch.max(outputs, 1)
            _, true_labels = torch.max(labels, 1)
            correct += (predicted == true_labels).sum().item()
            total += labels.size(0)

        epoch_accuracy = correct / total

        print(f"Epoch {epoch + 1}, Loss: {running_loss / len(train_loader):.4f}, Accuracy: {epoch_accuracy * 100:.2f}%")


def evaluate_model(model, test_loader, device):
    model.eval()
    all_true_labels = []
    all_pred_labels = []
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)

            _, predicted = torch.max(outputs, 1)
            _, true_labels = torch.max(labels, 1)
            all_true_labels.extend(true_labels.cpu().numpy())
            all_pred_labels.extend(predicted.cpu().numpy())

    cm = confusion_matrix(all_true_labels, all_pred_labels)
    accuracy = np.trace(cm) / np.sum(cm)
    print(f"Test Accuracy: {accuracy * 100:.2f}%")

    misclassified_counts = cm.sum(axis=1) - np.diag(cm)
    for label_idx, count in enumerate(misclassified_counts):
        print(f"Label {label_idx} misclassified {count} times.")
