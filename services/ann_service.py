import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam
from typing import Dict, List, Any, Tuple

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
    lag: int = 3,
    epochs: int = 150,
    batch_size: int = 2,
    learning_rate: float = 0.01,
    dropout_rate: float = 0.1,
    hidden_neurons: List[int] = [16, 8]
) -> Dict[str, Any]:
    """
    Trains an ANN model on the 17-month series and forecasts the 18th month.
    """
    if len(series) < lag + 1:
        raise ValueError(f"Jumlah data ({len(series)}) terlalu sedikit untuk lag = {lag}.")

    # 1. Prepare supervised learning datasets
    X_raw, y_raw = prepare_sliding_window_data(series, lag)

    # 2. Normalize data using MinMax scaling
    # Fit scaler on features + target combined to preserve relation, or separately
    scaler_x = MinMaxScaleHelper()
    scaler_y = MinMaxScaleHelper()

    X_scaled = scaler_x.fit_transform(X_raw)
    y_scaled = scaler_y.fit_transform(y_raw)

    # 3. Build Keras Sequential ANN Model
    model = Sequential()
    # Input layer
    model.add(Input(shape=(lag,)))
    
    # Hidden layers
    for neurons in hidden_neurons:
        model.add(Dense(neurons, activation="relu"))
        if dropout_rate > 0:
            model.add(Dropout(dropout_rate))
            
    # Output layer (linear activation for regression)
    model.add(Dense(1, activation="linear"))

    # 4. Compile model with Adam optimizer and MSE loss
    optimizer = Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss="mean_squared_error")

    # 5. Train model
    history = model.fit(
        X_scaled,
        y_scaled,
        epochs=epochs,
        batch_size=batch_size,
        verbose=0  # Silent training
    )

    # Extract loss history (MSE)
    loss_history = [float(loss) for loss in history.history["loss"]]

    # 6. Predict next value (18th month)
    # The feature input for the 18th month is the last 'lag' elements of our original series
    last_window = np.array([series[-lag:]], dtype=np.float32)
    last_window_scaled = scaler_x.transform(last_window)
    
    scaled_prediction = model.predict(last_window_scaled, verbose=0)
    prediction = scaler_y.inverse_transform(float(scaled_prediction[0][0]))

    # Calculate train predictions to measure fit
    scaled_train_pred = model.predict(X_scaled, verbose=0)
    train_predictions = [scaler_y.inverse_transform(float(val[0])) for val in scaled_train_pred]

    return {
        "forecast_value": float(round(prediction, 4)),
        "loss_history": loss_history,
        "final_loss": float(loss_history[-1]),
        "train_predictions": train_predictions,
        "actual_values": [float(y) for y in y_raw],
        "parameters": {
            "lag": lag,
            "epochs": epochs,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            "dropout_rate": dropout_rate,
            "hidden_neurons": hidden_neurons
        }
    }
