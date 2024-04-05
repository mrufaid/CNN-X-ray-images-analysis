# -*- coding: utf-8 -*-
"""X_ray.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gfmBGDG8vfGSvJ7YSfn_yFRc-AXtFAQ-

Download the dataset from the following link:
https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia?select=chest_xray

# Part 1: Image loading and preprocessing
"""

import zipfile
import glob
import cv2
import matplotlib.pyplot as plt

import numpy as np

def img_preprocess(img):
  img=cv2.imread(img)
  img= cv2.resize(img, (100,75))
  img= img/255.0
  return img

from google.colab import drive
drive.mount('/content/drive')

with zipfile.ZipFile('/content/drive/MyDrive/x-ray.zip', 'r') as zip_ref:
    zip_ref.extractall('/content')

"""## Prepare training dataset and preprocess images"""

normal_files_paths= glob.glob(r'/content/chest_xray/chest_xray/train/NORMAL/*.jpeg')
pneu_files_paths= glob.glob(r'/content/chest_xray/chest_xray/train/PNEUMONIA/*.jpeg')

normal_files_paths_val=glob.glob(r'/content/chest_xray/chest_xray/val/NORMAL/*jpeg')
pneu_files_paths_val=glob.glob(r'/content/chest_xray/chest_xray/val/PNEUMONIA/*jpeg')

normal_files_paths_test=glob.glob(r'/content/chest_xray/chest_xray/test/NORMAL/*jpeg')
pneu_files_paths_test=glob.glob(r'/content/chest_xray/chest_xray/test/PNEUMONIA/*jpeg')

normal_files_paths= normal_files_paths+normal_files_paths_test+normal_files_paths_val

pneu_files_paths=pneu_files_paths+pneu_files_paths_test+pneu_files_paths_val

normal_images=[]


for files in normal_files_paths:
  img=img_preprocess(files)
  normal_images.append(img)
normal_images=np.array(normal_images)

pneu_images=[]
for files in pneu_files_paths:
  img=img_preprocess(files)
  pneu_images.append(img)
pneu_images=np.array(pneu_images)

X=np.vstack((normal_images,pneu_images))
X.shape

#create labels
labels1= np.zeros(len(normal_files_paths))
labels2 = np.ones(len(pneu_files_paths))
y= np.hstack((labels1, labels2))

"""---
#Part 2: Neural Network Part
"""

import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

y = to_categorical(y)

# First split to create training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=42)

# Second split to create training and validation sets from the training set
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=42)

"""#test"""

#define Convolutional Neura Network
def Conv_model():
    model= models.Sequential()
    model.add(layers.Conv2D(30,(3,3),input_shape=(75,100,3),activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2,2)))

    model.add(layers.Conv2D(60, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Conv2D(120, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))


    model.add(layers.Flatten())
    model.add(layers.Dense(32, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(2, activation='softmax'))
    model.compile(optimizer=Adam(learning_rate=0.0001 ), loss='categorical_crossentropy', metrics=['accuracy'])
    return model

model= Conv_model()
print(model.summary())

history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=12)

#create chart of progress
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Loss')
plt.xlabel('epoch')

#Plot performance(accuracy) per epoch

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.legend(['training','test'])
plt.title('Accuracy')
plt.xlabel('epoch')

# Assuming you have already imported the necessary libraries and trained your model

# Test the model on the test set
y_pred = model.predict(X_test)

# Evaluate the model performance

y_pred=np.argmax(y_pred, axis=1)
y_test=np.argmax(y_test, axis=1)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Generate classification report
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Generate confusion matrix
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

import seaborn as sns

# Plot confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix')
plt.show()
