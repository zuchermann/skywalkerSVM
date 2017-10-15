import glob
import os
import numpy as np
import scipy
import progressbar
import h5py
from PIL import Image
from skimage.measure import block_reduce
from skimage.feature import hog
from  scipy import ndimage
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(dir_path, os.pardir))

def get_image_data(directory):
    images = []
    #images
    num_images = len(glob.glob(directory + '/*.png'))
    print("Unpacking images...")
    with progressbar.ProgressBar(max_value=num_images) as bar:
        for i in range(num_images):
            image = scipy.ndimage.imread(os.path.join(directory, 'hand.mov_' + str(i) + '.png'), mode='L')
            images.append(image)
            bar.update(i)
    #data
    data_file = open(directory + "/data.txt", "r")
    data = []
    for line in data_file:
        val = line.split(", ")[1]
        val = val.replace(';\n','')
        val = val.split(' ')
        for i in range(len(val)):
            val[i] = int(val[i])
        data.append(val)
    return images, data

def get_image_h5(directory):
    with h5py.File(directory + '/image_data.h5', 'r') as hf:
        images = hf['images'][:]
        data = (hf['data'][:]).tolist()
    return images, data


def downsample_images(images, size = 12, flatten=True):
    reduced_images = []
    for image in images:
        reduced_image = block_reduce(image, block_size=(size, size), func=np.median)
        shape = reduced_image.shape
        if flatten:
            reduced_image = reduced_image.flatten()
        reduced_image = reduced_image.astype('uint8')
        reduced_images.append(reduced_image)
    #print('Reduced size:', str(shape))
    return reduced_images, shape

def crop(images):
    cropped = []
    for i in range(len(images)):
        cropped.append((images[i])[:,50:540])
    return cropped

def my_hog(images):
    hogs = []
    for i in range(len(images)):
        hg = hog(images[i], orientations=4, pixels_per_cell=(4, 4), cells_per_block=(4, 4), transform_sqrt=True)
        hogs.append(hg)
    return hogs


def fist_to_binary(data):
    ##IN PLACE
    #converts 0,0,0,0,0 to 1
    #and 99,99,99,99,99 to 0
    for i in range(len(data)):
        data[i] = 1 if data[i] == [0, 0, 0, 0, 0] else 0

def fingers_to_classes(data):
    ##IN PLACE
    ##like fist to binary but different class for each finger
    for i in range(len(data)):
        val = 0
        if data[i] == [99, 0, 0, 0, 0]:
            val = 1
        elif data[i] == [0, 99, 0, 0, 0]:
            val = 2
        elif data[i] == [0, 0, 99, 0, 0]:
            val = 3
        elif data[i] == [0, 0, 0, 99, 0]:
            val = 4
        elif data[i] == [0, 0, 0, 0, 99]:
            val = 5
        data[i] = val

def finger_to_regression_label(data, finger_index):
    ##IN PLACE
    ##extracts data for single finger to be used in regression
    for i in range(len(data)):
        data[i] = data[i][finger_index]



def split_sets(images, data, indexes, prop_train):
    #prop train is proprtion that will be reserved for training
    num_images = len(images)
    index_train = int(num_images * prop_train)
    train_images = []
    test_images = []
    train_data = []
    test_data = []
    for i in range(num_images):
        rand_index = indexes[i]
        if i < index_train:
            train_images.append(images[rand_index])
            train_data.append(data[rand_index])
        else:
            test_images.append(images[rand_index])
            test_data.append(data[rand_index])
    return train_images, test_images, train_data, test_data


def screenshot(x1, y1, x2, y2, sct):
    monitors = sct.enum_display_monitors()

    # With the mss().
    raw = sct.get_pixels(monitors[1])
    size = (sct.width, sct.height)
    img = Image.frombytes('RGB',
                          size,
                          sct.image)
    all_pixels = np.array(img.convert('L'))
    selected_pixels = all_pixels[y1:y2, x1:x2]
    return selected_pixels
