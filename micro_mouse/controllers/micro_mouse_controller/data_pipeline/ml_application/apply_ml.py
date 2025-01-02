from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd


def preprocess(data):
    data['prev_yaw'] = data['yaw'].shift(1, fill_value=0)

    X = data[['front-dist', 'right-dist', 'rear-dist', 'left-dist', 'prev_yaw']]
    y = data['direction']

    label_mapping = {-1: 0, 0: 1, 1: 2}
    y_mapped = y.map(label_mapping)

    scaler = StandardScaler()
    X_scalered = scaler.fit_transform(X)

    return X, y_mapped, scaler


def train_rf_model():
    data = pd.read_excel("data_pipeline/data/robot_navigation_data.xlsx")
    X, y, scaler = preprocess(data)

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        random_state=42
    )

    model.fit(X, y)
    print("RandomForestClassifier model trained successfully!")

    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)
    print(f"RandomForestClassifier Results:", accuracy)

    return model, scaler


def train_xgb_model():
    data = pd.read_excel("data_pipeline/data/downsampled_robot_navigation_data.xlsx")
    X, y, scaler = preprocess(data)

    model = XGBClassifier(
        n_estimators=500,
        max_depth=10,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )

    model.fit(X, y)
    print("XGBClassifier model trained successfully!")

    return model, scaler


def train_mlp_model():
    data = pd.read_excel("data_pipeline/data/robot_navigation_data.xlsx")

    X, y, scaler = preprocess(data)

    model = MLPClassifier(
        hidden_layer_sizes=(256, 128, 64),
        activation='relu',
        solver='adam',
        learning_rate_init=0.001,
        max_iter=2000,
        random_state=42
    )

    model.fit(X, y)
    print("MLP model trained successfully!")

    return model, scaler


def preprocess_new_position(new_position):
    expected_columns = ['front-dist', 'right-dist', 'rear-dist', 'left-dist', 'prev_yaw']
    data = pd.DataFrame(new_position, columns=expected_columns)
    return data


def predict(model, scaler, new_position):
    #new_position = scaler.transform(preprocess_new_position(new_position))

    predicted_class = model.predict(preprocess_new_position(new_position))

    label_mapping = {0: -1, 1: 0, 2: 1}

    # Map predicted class back to original labels (-1, 0, or 1)
    original_class = [label_mapping[label] for label in predicted_class]

    return original_class[0]