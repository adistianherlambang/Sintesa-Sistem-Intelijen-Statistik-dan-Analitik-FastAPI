import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam
from typing import Dict, List, Any, Tuple
import threading

# Global thread-safe model cache
_MODEL_CACHE = {}
_cache_lock = threading.Lock()

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

def get_cached_model_and_train_func(lag: int, hidden_neurons: List[int], dropout_rate: float, learning_rate: float):
    """
    Retrieves or creates a cached Keras model, its compiled tf.function training loop,
    initial weights, and optimizer instance to completely avoid re-compilation.
    """
    cache_key = (lag, tuple(hidden_neurons), dropout_rate, learning_rate)
    with _cache_lock:
        if cache_key in _MODEL_CACHE:
            return _MODEL_CACHE[cache_key]

        # 1. Build Keras Sequential ANN Model
        model = Sequential()
        model.add(Input(shape=(lag,)))
        for neurons in hidden_neurons:
            model.add(Dense(neurons, activation="relu"))
            if dropout_rate > 0:
                model.add(Dropout(dropout_rate))
        model.add(Dense(1, activation="linear"))

        initial_weights = model.get_weights()
        optimizer = Adam(learning_rate=learning_rate)

        # 2. Define fully compiled training loop for this specific model architecture
        @tf.function
        def train_full_ann(X_data, y_data, epochs_val, batch_size_val):
            n_samples = tf.shape(X_data)[0]
            loss_history_tensor = tf.TensorArray(dtype=tf.float32, size=epochs_val)
            
            for epoch in tf.range(epochs_val):
                epoch_loss_sum = tf.constant(0.0)
                steps = tf.constant(0.0)
                
                # Simple batch iteration
                for i in tf.range(0, n_samples, batch_size_val):
                    x_batch = X_data[i:i+batch_size_val]
                    y_batch = y_data[i:i+batch_size_val]
                    
                    with tf.GradientTape() as tape:
                        y_pred = model(x_batch, training=True)
                        loss = tf.reduce_mean(tf.square(y_batch - y_pred))
                    grads = tape.gradient(loss, model.trainable_variables)
                    optimizer.apply_gradients(zip(grads, model.trainable_variables))
                    
                    epoch_loss_sum += loss
                    steps += 1.0
                    
                loss_history_tensor = loss_history_tensor.write(epoch, epoch_loss_sum / steps)
                
            return loss_history_tensor.stack()

        _MODEL_CACHE[cache_key] = (model, train_full_ann, initial_weights, optimizer)
        return _MODEL_CACHE[cache_key]

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
    Highly optimized using tf.function graph compilation with model weight/optimizer resets.
    """
    if len(series) < lag + 1:
        raise ValueError(f"Jumlah data ({len(series)}) terlalu sedikit untuk lag = {lag}.")

    # 1. Prepare supervised learning datasets
    X_raw, y_raw = prepare_sliding_window_data(series, lag)

    # 2. Normalize data using MinMax scaling
    scaler_x = MinMaxScaleHelper()
    scaler_y = MinMaxScaleHelper()

    X_scaled = scaler_x.fit_transform(X_raw)
    y_scaled = scaler_y.fit_transform(y_raw)

    # 3. Retrieve cached compiled model components
    model, train_func, initial_weights, optimizer = get_cached_model_and_train_func(
        lag=lag,
        hidden_neurons=hidden_neurons,
        dropout_rate=dropout_rate,
        learning_rate=learning_rate
    )

    # 4. Reset weights and optimizer state to clean slate
    model.set_weights(initial_weights)
    for var in optimizer.variables:
        var.assign(tf.zeros_like(var))

    # Convert inputs to Tensors
    X_tensor = tf.convert_to_tensor(X_scaled, dtype=tf.float32)
    y_tensor = tf.convert_to_tensor(y_scaled, dtype=tf.float32)

    # 5. Execute compiled training graph
    loss_history_vals = train_func(X_tensor, y_tensor, epochs, batch_size)
    loss_history = [float(loss) for loss in loss_history_vals.numpy()]

    # 6. Predict next value (18th month)
    last_window = np.array([series[-lag:]], dtype=np.float32)
    last_window_scaled = scaler_x.transform(last_window)
    last_window_tensor = tf.convert_to_tensor(last_window_scaled, dtype=tf.float32)
    
    scaled_prediction = model(last_window_tensor, training=False)
    prediction = scaler_y.inverse_transform(float(scaled_prediction[0][0]))

    # Calculate train predictions to measure fit
    scaled_train_pred = model(X_tensor, training=False)
    train_predictions = [scaler_y.inverse_transform(float(val[0])) for val in scaled_train_pred.numpy()]

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
