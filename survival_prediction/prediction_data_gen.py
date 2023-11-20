import os
import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import statistics
from scipy.stats import weibull_min, weibull_max
from sklearn import preprocessing
import tensorflow as tf
from tensorflow.keras import initializers, regularizers
from tensorflow.keras import backend as k
from tensorflow.keras.layers import Input, multiply, Layer
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import RMSprop, SGD, Adam
from tensorflow.keras.models import Model
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
from lifelines.utils import concordance_index


# i don't know meaning, but i input just for making it running
n = 1
xi = 0
xj = 1


class DataGenerator(tf.keras.utils.Sequence):
    "Generates data for Keras"

    def __init__(
        self,
        patient_bar,
        labels,
        status,
        batch_size=32,
        dim=(299, 299),
        n_channels=3,
        folder="train",
        shuffle=False,
    ):

        "Initialization"
        self.dim = dim
        self.batch_size = batch_size
        self.labels = labels
        self.status = status
        self.patient_bar = patient_bar

        self.n_channels = n_channels
        self.shuffle = shuffle
        self.folder = folder
        self.on_epoch_end()

    def __len__(self):
        "Denotes the number of batches per epoch"
        return int(np.floor(len(self.patient_bar) / self.batch_size))

    def __getitem__(self, index):
        "Generate one batch of data"
        # Generate indexes of the batch
        indexes = self.indexes[index * self.batch_size : (index + 1) * self.batch_size]

        # Find list of IDs
        patient_bar_temp = [self.patient_bar[k] for k in indexes]

        # Generate data
        X_person, y = self.__data_generation(indexes)

        return X_person, y

    def on_epoch_end(self):
        "Updates indexes after each epoch"
        self.indexes = np.arange(len(self.patient_bar))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, patient_bar_temp):
        "Generates data containing batch_size samples"  # X : (n_samples, *dim, n_channels)

        train_df = pd.read_pickle("train_df.pkl")
        test_df = pd.read_pickle("test_df.pkl")

        real_day = list(train_df["Days"])
        int_day = map(int, real_day)
        real_day = list(int_day)
        day_mean = statistics.mean(real_day)
        day_std = statistics.stdev(real_day)
        Days_std = [
            ((i - day_mean) / day_std) + n for i in real_day
        ]  # please input n (make sure Days_std >0)

        train_df["Days_std"] = Days_std
        train_df = train_df.reset_index(drop=True)

        test_day = list(test_df["Days"])
        int_test = list(map(int, test_day))
        Days_std_test = [
            ((i - day_mean) / day_std) + n for i in int_test
        ]  # please input n

        test_df["Days_std"] = Days_std_test
        test_df = test_df.reset_index(drop=True)

        feature_columns = train_df.columns[xi:xj]  # select feature columns

        X_person = []

        y = []
        y_d = []
        y_s = []

        # Generate data
        for i, ID in enumerate(patient_bar_temp):
            train_array = []

            if self.folder == "train_df":
                per_person = train_df.loc[
                    train_df["bcr_patient_barcode"] == self.patient_bar[ID]
                ]  # select a person

            else:
                per_person = test_df.loc[
                    test_df["bcr_patient_barcode"] == self.patient_bar[ID]
                ]  # select a person

            per_person_array = (
                per_person[feature_columns]
            ).to_numpy()  # per person features to array
            train_array.append(per_person_array)

            X_person.append(train_array)

            y_d.append(list(per_person["Days"])[0])
            y_s.append(list(per_person["vital_status"])[0])

        X_person = np.array(X_person).squeeze()

        y_d = np.array(y_d).astype("float")[:, np.newaxis]

        y_s = np.array(y_s).astype("int")[:, np.newaxis]
        y_temp = np.hstack((y_d, y_s))

        y = tf.convert_to_tensor(y_temp, dtype=tf.float32)

        return X_person, y
