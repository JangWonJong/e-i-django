import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import datasets


class Solution:
    def __init__(self):
        self.mnist = keras.datasets.mnist

        (train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data()

        train_images = train_images.reshape((60000, 28, 28, 1))
        test_images = test_images.reshape((10000, 28, 28, 1))

        # 픽셀 값을 0~1 사이로 정규화합니다.
        train_images, test_images = train_images / 255.0, test_images / 255.0

    def solution(self):
        model = keras.models.Sequential()
        model.add(keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
        model.add(keras.layers.MaxPooling2D((2, 2)))
        model.add(keras.layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(keras.layers.MaxPooling2D((2, 2)))
        model.add(keras.layers.Conv2D(64, (3, 3), activation='relu'))

        model.summary()