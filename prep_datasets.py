# from google.colab import drive
from os import listdir
from os.path import isfile, join, getsize
import sys
import numpy as np
from PIL import Image
from matplotlib.pyplot import imshow

import matplotlib.pyplot as plt
import cv2
import math

path = './images/'

files_in_dir = [f for f in listdir(path) if isfile(join(path, f)) if getsize(join(path, f)) > 10]

# [-20:-4]

counter = 0
while counter < (len(files_in_dir) - 2):
    f1 = int(files_in_dir[counter][:-4]) + 20
    f2 = int(files_in_dir[counter+1][:-4])+10
    f3 = int(files_in_dir[counter+2][:-4])
    if f1 == f2 == f3:
        counter += 3
    else:
        files_in_dir.pop(counter)
        counter = 0



modular_3 = len(files_in_dir) % 3
if modular_3 != 0:
    files_in_dir = files_in_dir[:-modular_3]
mod_3_new = len(files_in_dir) % 3

numImages = len(files_in_dir)
# background_image = plt.imread('background.gif')

count = 0
rain_images = []
# files_in_dir = files_in_dir[:numImages]  # Reduce number of images for now to 60


for f in files_in_dir:  # Clean and crop each image
    s = join(path, files_in_dir[count])
    count += 1
    print(count)
    rain_image = plt.imread(s)
    height, width, depth = rain_image.shape

    # imgdiff = background_image - rain_image # Perform background suppression
    imggood = cv2.cvtColor(rain_image, cv2.COLOR_BGR2RGB) # Switch back to normal color encoding

    cropped = imggood[0:480, 0:480]  # Crop
    height, width, depth = cropped.shape
    resized = cv2.resize(cropped, (int(height / 7.5), int(width / 7.5)), interpolation = cv2.INTER_AREA)  # Resize to 64 by 64
    converted = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)
    converted = converted[..., np.newaxis]
    rain_images.append(np.asarray(converted))  # Add to new rain images list

# imshow(rain_images[0])  # Test output
# half_images = numImages // 2
half_images = math.floor(numImages * 0.8)
train_list = rain_images[:half_images]  # Split into 30 train and 30 test
test_list = rain_images[half_images:]

print('done loading images and converting to greyscale')

train_images = []
train_images_extra = []
train_labels = []
for i in range (0, len(train_list)):  # Split train into 20 images and 10 labels
  if i % 3 == 2:
    train_labels.append(np.ndarray.flatten(train_list[i]))
  elif i % 3 == 1:
    train_images_extra.append(train_list[i])
  else:
    train_images.append(train_list[i])


test_images = []
test_images_extra = []
test_labels = []
for i in range (0, len(test_list)):  # Split test into 20 images and 10 labels
  if i % 3 == 2:
    test_labels.append(np.ndarray.flatten(test_list[i]))
  elif i % 3 == 1:
    test_images_extra.append(test_list[i])
  else:
    test_images.append(test_list[i])

print('done separating training/testing images and labels')

good_train_images = []
for i in range(0, len(train_labels)):
  image = np.concatenate((train_images[i], train_images_extra[i]), 0)
  image = np.expand_dims(image, axis=0)
  good_train_images.append(image)

good_test_images = []
for i in range(0, len(test_labels)):
  image = np.concatenate((test_images[i], test_images_extra[i]), 0)
  image = np.expand_dims(image, axis=0)
  good_test_images.append(image)



good_train_images = np.concatenate((good_train_images), 0)
print(good_train_images.shape)

train_labels = np.asarray(train_labels)
print(train_labels.shape)

good_test_images = np.concatenate((good_test_images), 0)
print(good_test_images.shape)

test_labels = np.asarray(test_labels)
print(test_labels.shape)
#train_labels = np.concatenate((train_labels), 0)

np.save('./training_images_big.npy', good_train_images)
np.save('./training_labels_big.npy', train_labels)
np.save('./testing_images_big.npy', good_test_images)
np.save('./testing_labels_big.npy', test_labels)
print('done')

# good_train_images = np.load('/content/drive/My Drive/Skynet/training_images_big.npy')
# train_labels = np.load('/content/drive/My Drive/Skynet/training_labels_big.npy')
# good_test_images = np.load('/content/drive/My Drive/Skynet/testing_images_big.npy')
# test_labels = np.load('/content/drive/My Drive/Skynet/testing_labels_big.npy')

#print(train_labels.shape)

print('done')