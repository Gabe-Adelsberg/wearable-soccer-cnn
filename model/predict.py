from pathlib import Path

import numpy as np
from keras.models import load_model

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
MODEL_PATH = Path(__file__).resolve().parent / "CNNMain.keras"

CLASS_NAMES = ["shot", "pass", "dribble", "jogging"]


def main():
    model = load_model(MODEL_PATH)

    test_data = np.genfromtxt(DATA_DIR / "testData.csv", delimiter=",")
    test_labels = np.genfromtxt(DATA_DIR / "labelTest.csv", delimiter=",")

    # Preserved from the original project workflow.
    test_data = np.tile(test_data, (60, 1, 1))

    predictions = model.predict(test_data)
    predicted_classes = predictions.argmax(axis=-1)

    correct = 0
    for expected, predicted in zip(test_labels, predicted_classes):
        if int(expected) == int(predicted):
            correct += 1

    accuracy = correct / len(test_labels)
    print(f"Test Accuracy: {accuracy:.3f}")

    for index, predicted in enumerate(predicted_classes):
        label = CLASS_NAMES[int(predicted)] if int(predicted) < len(CLASS_NAMES) else str(predicted)
        print(f"Sample {index + 1}: {label}")


if __name__ == "__main__":
    main()
