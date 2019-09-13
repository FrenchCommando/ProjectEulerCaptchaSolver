# https://towardsdatascience.com/image-classification-in-10-minutes-with-mnist-dataset-54c35b77a38d
# https://machinelearningmastery.com/save-load-keras-deep-learning-models/
import os
import tensorflow as tf
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D


class Mnist:

    img_rows, img_cols = 28, 28
    path = "model.h5"
    @staticmethod
    def init_model():
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

        print(x_train.shape)
        n, img_rows, img_cols = x_train.shape

        # Reshaping the array to 4-dims so that it can work with the Keras API
        x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
        x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
        input_shape = (img_rows, img_cols, 1)

        # Making sure that the values are float so that we can get decimal points after division
        x_train = x_train.astype('float32')
        x_test = x_test.astype('float32')

        # Normalizing the RGB codes by dividing it to the max RGB value.
        x_train /= 255
        x_test /= 255
        print('x_train shape:', x_train.shape)
        print('Number of images in x_train', x_train.shape[0])
        print('Number of images in x_test', x_test.shape[0])

        # Creating a Sequential Model and adding the layers
        model = Sequential()
        model.add(Conv2D(28, kernel_size=(3, 3), input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())  # Flattening the 2D arrays for fully connected layers
        model.add(Dense(128, activation=tf.nn.relu))
        model.add(Dropout(0.2))
        model.add(Dense(10, activation=tf.nn.softmax))

        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        model.fit(x=x_train, y=y_train, epochs=10)

        # model.evaluate(x_test, y_test)

        # save model and architecture to single file
        model.save(Mnist.path)
        print("Saved model to disk")

    def __init__(self):
        if not os.path.exists(Mnist.path):
            Mnist.init_model()
        # load model
        self.model = load_model('model.h5')

    def guess(self, image):
        pred = self.model.predict(image.reshape(1, Mnist.img_rows, Mnist.img_cols, 1))  # .transpose())
        return pred.argmax()
