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
    images, shape = downsample_images(images, 45)
    return images, shape


##importing images
thumb_images, thumb_data = get_image_h5("./../data/with_brace/ipad_zach/thumb_cont") # get images
thumb_images, thumb_shape = prepare(thumb_images)

pointer_images, pointer_data = get_image_h5("./../data/with_brace/ipad_zach/pointer_cont2") # get images
pointer_images, pointer_shape = prepare(pointer_images)

middle_images, middle_data = get_image_h5("./../data/with_brace/ipad_zach/middle_cont") # get images
middle_images, middle_shape = prepare(middle_images)

ring_images, ring_data = get_image_h5("./../data/with_brace/ipad_zach/ring_cont") # get images
ring_images, ring_shape = prepare(ring_images)

pinky_images, pinky_data = get_image_h5("./../data/with_brace/ipad_zach/pinky_cont") # get images
pinky_images, pinky_shape = prepare(pinky_images)

##convert label data to two classes
finger_to_regression_label(thumb_data, 0)
finger_to_regression_label(pointer_data, 1) # prepare data for pointer finger
finger_to_regression_label(middle_data, 2)
finger_to_regression_label(ring_data, 3)
finger_to_regression_label(pinky_data, 4)

##test display image
#image = Image.fromarray(images[0].reshape(shape))
#image.show()

## Create a classifier: a support vector regressor
thumb = svm.SVR(gamma=0.00006)
thumb.fit(thumb_images, thumb_data)

pointer = svm.SVR(gamma=0.00006)
pointer.fit(pointer_images, pointer_data)

middle = svm.SVR(gamma=0.00006)
middle.fit(middle_images, middle_data)

ring = svm.SVR(gamma=0.00006)
ring.fit(ring_images, ring_data)

pinky = svm.SVR(gamma=0.00006)
pinky.fit(pinky_images, pinky_data)

## run the model
while True:
    sct = mss()
    input_image = screenshot(370, 80, 970, 820, sct) #bounds to be screenshot x1, y1, x2, y2
    input_image, shape = prepare([input_image])

    thumb_prediction = thumb.predict(input_image)
    pointer_prediction = pointer.predict(input_image)
    middle_prediction = middle.predict(input_image)
    ring_prediction = ring.predict(input_image)
    pinky_prediction = pinky.predict(input_image)
    #print(prediction)

    ## udp
    msg = str(thumb_prediction[0]) + " " + str(pointer_prediction[0]) + " " + str(middle_prediction[0]) + " " + str(ring_prediction[0]) + " " + str(pinky_prediction[0])
    sock.sendto(bytearray(msg, 'utf8'), (UDP_IP, SENDER_UDP_PORT))

    ## test output image
    #image = Image.fromarray(input_image[0].reshape(shape))
    #image.show()
    #break