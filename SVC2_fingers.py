import random
from util import *
from sklearn import svm, metrics
from PIL import Image

##importing images
images, data = get_image_h5("./../data/with_brace/jason/binary_3") # get images
test_images, test_data = get_image_h5("./../data/with_brace/jason/binary_2") # get images
images = crop(images)
test_images = crop(test_images)
images, shape = downsample_images(images, 32)
test_images, test_shape = downsample_images(test_images, 32)

##convert label data to two classes
fingers_to_classes(data)
fingers_to_classes(test_data)

##shuffle and split into training/test sets
#indexes = [i for i in range(len(images))]
#random.shuffle(indexes)
#train_prop = 0.5
#train_images, test_images, train_data, test_data = split_sets(images, data, indexes, train_prop)

##test display image
image = Image.fromarray(images[0].reshape(shape))
image.show()

## Create a classifier: a support vector classifier
classifier = svm.SVC(gamma=0.00001)
classifier.fit(images, data)



## Predict fist open vs closed based on remaining images
expected = test_data
predicted = classifier.predict(test_images)

print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(expected, predicted)))
print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))