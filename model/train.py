from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from keras.layers import Conv1D, Dense, Dropout, Flatten, MaxPooling1D
from keras.models import Sequential
from keras.utils import to_categorical

NUM_CLASSES = 4
INPUT_SHAPE = (420, 6)
DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_dataset(data_name: str, label_name: str):
    data = np.genfromtxt(DATA_DIR / data_name, delimiter=",")
    labels = np.genfromtxt(DATA_DIR / label_name, delimiter=",")

    # This mirrors the structure preserved in the original research code.
    # The original project duplicated each collected window before training.
    data = np.tile(data, (60, 1, 1))
    labels = to_categorical(labels, num_classes=NUM_CLASSES)
    return data, labels


def build_model():
    model = Sequential(
        [
            Conv1D(32, kernel_size=3, activation="relu", input_shape=INPUT_SHAPE),
            MaxPooling1D(pool_size=2),
            Conv1D(64, kernel_size=3, activation="relu"),
            MaxPooling1D(pool_size=2),
            Flatten(),
            Dense(128, activation="relu"),
            Dropout(0.5),
            Dense(NUM_CLASSES, activation="softmax"),
        ]
    )

    model.compile(
        loss="categorical_crossentropy",
        optimizer="adam",
        metrics=["accuracy"],
    )
    return model


def plot_history(history, dataset_number: int):
    plt.figure()
    plt.plot(history.history["accuracy"])
    plt.plot(history.history["val_accuracy"])
    plt.title(f"Model Accuracy - Dataset {dataset_number}")
    plt.ylabel("Accuracy")
    plt.xlabel("Epoch")
    plt.legend(["Train", "Validation"], loc="upper left")
    plt.show()

    plt.figure()
    plt.plot(history.history["loss"])
    plt.plot(history.history["val_loss"])
    plt.title(f"Model Loss - Dataset {dataset_number}")
    plt.ylabel("Loss")
    plt.xlabel("Epoch")
    plt.legend(["Train", "Validation"], loc="upper left")
    plt.show()


def main():
    datasets = [
        ("TrainingOne.csv", "LabelOne.csv"),
        ("TrainingTwo.csv", "LabelTwo.csv"),
        ("TrainingThree.csv", "LabelThree.csv"),
    ]

    model = build_model()
    model.summary()

    histories = []
    for data_name, label_name in datasets:
        training_data, labels = load_dataset(data_name, label_name)
        history = model.fit(
            training_data,
            labels,
            epochs=10,
            batch_size=32,
            validation_split=0.2,
        )
        histories.append(history)

    model.save("CNNMain.keras")

    for index, history in enumerate(histories, start=1):
        plot_history(history, index)


if __name__ == "__main__":
    main()
