
# X-Ray Image Classification

This project aims to classify X-ray images into two categories: normal and pneumonia. It uses convolutional neural networks (CNNs) implemented in TensorFlow/Keras.

## Dataset

The dataset consists of X-ray images of chest scans, categorized into normal and pneumonia cases. The dataset is split into training, validation, and test sets.

## Model

The neural network model is a CNN architecture with several convolutional layers followed by max-pooling layers and fully connected layers. The final layer uses the softmax activation function for binary classification.

## Usage

1. Clone the repository:

```bash
git clone https://github.com/mrufaid/CNN-X-ray-images-analysis.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the main script to train the model:

```bash
x_ray.py
```



## Results

The trained model achieves an accuracy of [95.22%] on the test set. The confusion matrix and classification report are also provided for detailed evaluation.

## Author

- [Muhammad Rufaid Peerzada](https://github.com/mrufaid)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
```
