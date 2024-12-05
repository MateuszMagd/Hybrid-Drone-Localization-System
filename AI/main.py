import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

print(f"TensorFlow version: {tf.__version__}")
print(f"Keras module: {Sequential}")

if __name__ == '__main__':
    # Definicja modelu
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(patch_size, patch_size, 1)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(2, activation='linear')  # Wynikiem są współrzędne [latitude, longitude]
    ])

    # Kompilacja modelu
    model.compile(optimizer='adam', loss='mean_squared_error')