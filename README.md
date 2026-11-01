# Wearable Soccer Action Classification with a 1D CNN

A wearable-sensor and machine-learning project designed to classify soccer actions using inertial measurements collected from a custom Arduino-based device.

## Project Overview

The project combined embedded sensing with a one-dimensional convolutional neural network. A wearable device collected six-axis inertial data from a BMI160 IMU, stored the measurements to an SD card, and supplied the resulting datasets to a TensorFlow/Keras CNN for action classification.

The target classes were:

- Shot
- Pass
- Dribble
- Jogging

The complete workflow was:

**IMU sensing → Arduino data acquisition → SD-card logging → dataset preparation → CNN training → action classification**

## Hardware

- Arduino Nano Every
- DFRobot BMI160 6-DOF IMU
- SD-card module
- USB battery supply
- Wearable mounting hardware

The BMI160 provided three-axis gyroscope data and three-axis acceleration data, giving six input channels per sample.

## Software

- Arduino / C++
- Python
- TensorFlow / Keras
- NumPy
- Matplotlib

## CNN Architecture

The research implementation used a 1D CNN with:

- Input shape: `420 x 6`
- Conv1D layer with 32 filters
- Max-pooling layer
- Conv1D layer with 64 filters
- Max-pooling layer
- Flatten layer
- Dense layer with 128 units and ReLU
- Dropout regularization
- Four-class softmax output

## Repository Structure

```text
wearable-soccer-cnn/
├── README.md
├── firmware/
│   └── wearable_sensor.ino
├── model/
│   ├── train.py
│   └── predict.py
├── data/
│   └── README.md
├── requirements.txt
└── .gitignore
```

## Source-Code Note

The source files in this repository were reconstructed and cleaned from the code preserved in the appendix of my original research paper. The intent is to preserve the original project design while making the code readable and usable as a portfolio artifact.

## Research Context

The project investigated whether wearable inertial sensors combined with convolutional neural networks could classify soccer actions and provide a foundation for data-driven training analysis.

Training data was collected during organized soccer drills, manually labeled by action, and divided into training and validation sets. A separate dataset was reserved for prediction testing.

## Future Improvements

- Recover and publish the original labeled datasets where appropriate
- Add confusion-matrix and per-class evaluation metrics
- Normalize IMU inputs before training
- Replace repeated dataset tiling with proper time-window segmentation
- Add automated preprocessing and train/test splitting
- Deploy inference to an edge device for near-real-time classification
- Add enclosure and wearable-system photos
