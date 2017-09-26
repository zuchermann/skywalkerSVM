import random
from util import *
from sklearn import svm, metrics
from PIL import Image

##importing images
images, data = get_image_h5("./../data/with_brace/sonostar/binary_fist_small") # get images
images, shape = downsample_images(images)

##convert label data to two classes
fist_to_binary(data)

##shuffle and split into training/test sets
indexes = [i for i in range(len(images))]
random.shuffle(indexes)
train_prop = 0.25
train_images, test_images, train_data, test_data = split_sets(images, data, indexes, train_prop)

##test display image
#image = Image.fromarray(train_images[0].reshape(shape))
#image.show()

## Create a classifier: a support vector classifier
classifier = svm.SVC(gamma=0.000001)
classifier.fit(train_images, train_data)

## Predict fist open vs closed based on remaining images
expected = test_data
predicted = classifier.predict(test_images)

print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(expected, predicted)))
print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))