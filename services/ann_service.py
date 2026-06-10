import os
import json
import numpy as np
import tensorflow as tf
from typing import Dict, List, Any, Tuple

# Path configurations
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

def prepare_sliding_window_data(series: List[float], lag: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Transforms a univariate series into X (features) and y (targets) using sliding window.
    """
    X, y = [], []
    for i in range(len(series) - lag):
        X.append(series[i:i + lag])
        y.append(series[i + lag])
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)

class MinMaxScaleHelper:
    def __init__(self):
        self.min_val = 0.0
        self.max_val = 1.0
        self.eps = 1e-8

    def fit_transform(self, data: np.ndarray) -> np.ndarray:
        self.min_val = float(np.min(data))
        self.max_val = float(np.max(data))
        denom = self.max_val - self.min_val
        if abs(denom) < self.eps:
            denom = self.eps
        return (data - self.min_val) / denom

    def transform(self, data: np.ndarray) -> np.ndarray:
        denom = self.max_val - self.min_val
        if abs(denom) < self.eps:
            denom = self.eps
        return (data - self.min_val) / denom

    def inverse_transform(self, scaled_data: float) -> float:
        denom = self.max_val - self.min_val
        return float(scaled_data * denom + self.min_val)

def train_and_forecast(
    series: List[float],
    city_name: str,
    var_name: str,
    lag: int = 3,
    epochs: int = 150,
    batch_size: int = 2,
    learning_rate: float = 0.01,
    dropout_rate: float = 0.1,
    hidden_neurons: List[int] = [16, 8]
) -> Dict[str, Any]:
    """
    Tries to load model offline for forecasting. If it does not exist,
    runs the train service to build & save it first, then does inference.
    """
    from train.train_service import slugify
    city_slug = slugify(city_name)
    var_slug = slugify(var_name)
    
    model_path = os.path.join(MODELS_DIR, f"{city_slug}_{var_slug}.keras")
    meta_path = os.path.join(MODELS_DIR, f"{city_slug}_{var_slug}_meta.json")
    
    # Check if files exist
    if not (os.path.exists(model_path) and os.path.exists(meta_path)):
        print(f"[Inference] Model or metadata not found. Training model for {city_name} - {var_name}...")
        from train.train_service import train_and_save_model
        train_and_save_model(
            series=series,
            city_name=city_name,
            var_name=var_name,
            lag=lag,
            epochs=epochs,
            batch_size=batch_size,
            learning_rate=learning_rate,
            dropout_rate=dropout_rate,
            hidden_neurons=hidden_neurons
        )
        
    # Load model and metadata
    print(f"[Inference] Loading pre-trained model for {city_name} - {var_name}...")
    model = tf.keras.models.load_model(model_path)
    with open(meta_path, "r") as f:
        meta = json.load(f)
        
    # Scale last window
    last_window = np.array([series[-lag:]], dtype=np.float32)
    scaler_x_min = meta["scaler_x_min"]
    scaler_x_max = meta["scaler_x_max"]
    denom_x = scaler_x_max - scaler_x_min
    if abs(denom_x) < 1e-8:
        denom_x = 1e-8
    last_window_scaled = (last_window - scaler_x_min) / denom_x
    
    # Run prediction
    last_window_tensor = tf.convert_to_tensor(last_window_scaled, dtype=tf.float32)
    scaled_prediction = model(last_window_tensor, training=False)
    
    # Denormalize prediction
    scaler_y_min = meta["scaler_y_min"]
    scaler_y_max = meta["scaler_y_max"]
    prediction = float(scaled_prediction[0][0]) * (scaler_y_max - scaler_y_min) + scaler_y_min
    
    return {
        "forecast_value": float(round(prediction, 4)),
        "loss_history": meta["loss_history"],
        "final_loss": meta["final_loss"],
        "train_predictions": meta["train_predictions"],
        "actual_values": meta["actual_values"],
        "parameters": meta["parameters"]
    }
