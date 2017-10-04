from util import *
from sklearn import svm, metrics
from mss.factory import mss
import socket

## udp
UDP_PORT = 30330  # Port to listen and send udp messages.
UDP_IP = '127.0.0.1'
SENDER_UDP_PORT = 30328
sock = socket.socket(socket.AF_INET, # Internet
                       socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

def prepare(images):
    images = crop(images)
    images, shape = downsample_images(images, 64)
    return images, shape


##importing images
images, data = get_image_h5("./../data/with_brace/jason/oneMinute2") # get images
images, shape = prepare(images)

##convert label data to two classes
fingers_to_classes(data)

##test display image
#image = Image.fromarray(images[0].reshape(shape))
#image.show()

## Create a classifier: a support vector classifier
classifier = svm.SVC(gamma=0.00001)
classifier.fit(images, data)

## run the model
while True:
    sct = mss()
    input_image = screenshot(370, 80, 970, 820, sct) #bounds to be screenshot x1, y1, x2, y2
    input_image, shape = prepare([input_image])
    prediction = classifier.predict(input_image)
    print(prediction)

    ## udp
    msg = str(prediction[0])
    sock.sendto(bytearray(msg, 'utf8'), (UDP_IP, SENDER_UDP_PORT))

    ## test output image
    #image = Image.fromarray(input_image[0].reshape(shape))
    #image.show()
    #break