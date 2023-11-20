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

from prediction_model import *
from prediction_data_gen import *

# Survival dataframe
# data = {
#     'bcr_patient_barcode' : patient id,
#     'vital_status' : overalall survival status or disease free status,
#     'Days' : overalall survival days or disease free days
#     '0' : pathology image feature (dimension 1)
#     '1' : pathology image feature (dimension 2)
#     ...
#     'n' : pathology image feature (dimension n)
# }
# df = pd.DataFrame(data)

# please modify them urself
loss_function = weibull_loglik_discrete
optimizer = Adam(lr=0.0001)
epochs = 1

test_data1 = {
    "bcr_patient_barcode": [1, 2, 3],
    "vital_status": [1, 1, 1],
    "Days": [1, 2, 3],
    "0": [2, 2, 2],
    "1": [3, 3, 3],
    "2": [4, 4, 4],
    "3": [5, 3, 3],
}

stage12_fold1 = pd.DataFrame(test_data1)
stage12_fold2 = pd.DataFrame(test_data1)
stage12_fold3 = pd.DataFrame(test_data1)
stage12_fold4 = pd.DataFrame(test_data1)
stage12_fold5 = pd.DataFrame(test_data1)


train_df = pd.concat([stage12_fold1, stage12_fold2, stage12_fold3, stage12_fold4])
test_df = stage12_fold5
train_df = train_df.reset_index(drop=True)
test_df = test_df.reset_index(drop=True)

# train_df.to_pickle("train_df.pkl")
# test_df.to_pickle("test_df.pkl")

train_labels = train_df["Days"]
train_status = train_df["vital_status"]
train_bar = list(set(train_df["bcr_patient_barcode"]))

test_labels = test_df["Days"]
test_status = test_df["vital_status"]
test_bar = list(set(test_df["bcr_patient_barcode"]))

params_train = {
    "dim": (299, 299),
    "batch_size": 1,
    "n_channels": 3,
    "shuffle": False,
    "folder": "train_df",
}
params_test = {
    "dim": (299, 299),
    "batch_size": 1,
    "n_channels": 3,
    "shuffle": False,
    "folder": "test_df",
}

# Generators
training_generator = DataGenerator(
    train_bar, train_labels, train_status, **params_train
)
validation_generator = DataGenerator(test_bar, test_labels, test_status, **params_test)

data_input = Input(shape=(2048), dtype="float32", name="input")
alpha = Mil_Attention(
    L_dim=2048,
    output_dim=2,
    kernel_regularizer=l2(0.000001),
    name="alpha",
    use_gated="False",
)(data_input)
x_mul = multiply([alpha, data_input])
out = Last_Sigmoid(output_dim=2, name="FC1_sigmoid")(x_mul)
x_out = out
model = Model(inputs=data_input, outputs=x_out)

model.compile(
    loss=loss_function, optimizer=optimizer
)  # please input loss function,optimizer

model.fit(
    training_generator,
    validation_data=validation_generator,
    epochs=epochs,  # please input epochs
)

print("DONE")
