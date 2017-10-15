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
    #hogs = my_hog(images)
    return images


##importing images
ring_images, ring_data = get_image_h5("./../data/with_brace/ipad_zach/ring_cont2") # get images
ring_images = prepare(ring_images)

pinky_images, pinky_data = get_image_h5("./../data/with_brace/ipad_zach/pinky_cont2") # get images
pinky_images = prepare(pinky_images)

##convert label data to tvisualize=Truewo classes
finger_to_regression_label(ring_data, 3)
finger_to_regression_label(pinky_data, 4)

##test display image
#image = Image.fromarray(images[0].reshape(shape))
#image.show()

## Create a classifier: a support vector regressor
ring = svm.SVR(gamma=0.00006)
ring.fit(ring_images, ring_data)

pinky = svm.SVR(gamma=0.00006)
pinky.fit(pinky_images, pinky_data)

## run the model
while True:
    sct = mss()
    #times 2 on dimensions because retina bs
    input_image = screenshot(340*2, 80*2, 940*2, 820*2, sct) #bounds to be screenshot x1, y1, x2, y2
    input_image = block_reduce(input_image, block_size=(2, 2), func=np.median) # because retina crap
    input_image = prepare([input_image])

    ring_prediction = ring.predict(input_image)
    pinky_prediction = pinky.predict(input_image)
    print(pinky_prediction)

    ## udp
    msg = str('0' + " " + '0' + " " + '0' + " " + str(ring_prediction[0]) + " " + str(pinky_prediction[0]))
    sock.sendto(bytearray(msg, 'utf8'), (UDP_IP, SENDER_UDP_PORT))

    ## test output image
    #image = Image.fromarray(input_image[0].reshape(shape))
    #image.show()
    #break