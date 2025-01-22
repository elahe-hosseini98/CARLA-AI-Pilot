from autonomous_arena.training_pipeline import SimpleCNN
import cv2
import torch


def load_pretrained_model(path_2_model, num_classes=4, device="cpu"):
    model = SimpleCNN(num_classes).to(device)
    model.load_state_dict(torch.load(path_2_model))
    model.eval()
    print("Model loaded successfully")
    return model


def predict_new_action(model, image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    target_shape = (32, 14)
    resized_image = cv2.resize(gray_image, target_shape)

    normalized_image = resized_image / 255.0

    input_tensor = torch.tensor(normalized_image, dtype=torch.float32).unsqueeze(0).unsqueeze(0)

    device = next(model.parameters()).device
    input_tensor = input_tensor.to(device)

    model.eval()
    with torch.no_grad():
        output = model(input_tensor)
        predicted_class = torch.argmax(output, dim=1).item()

    return predicted_class
