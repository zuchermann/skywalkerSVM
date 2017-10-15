import socket
import threading
import time
import numpy as np
import os, shutil
import progressbar
from PIL import Image

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

label = '0 0 0 0 0'
images = []
labels = []


def listen_udp():
    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        new_label = data.decode("utf-8")
        global label
        label = new_label


udpThread = threading.Thread(target=listen_udp)
udpThread.start()

def record_image_data(data_queue):
    image = data_queue.get()
    images.append(image)
    labels.append(label)

def save_image_data():
    folder = 'images'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    with progressbar.ProgressBar(max_value=len(labels)) as bar:
        for i in range(len(labels)):
            cur_label = labels[i]
            image = Image.fromarray(images[i]).convert('RGB')
            image.save('images/hand.mov_'+ str(i) + '.png')
            bar.update(i)


##dummy random data meant to look like callback from bernie's code
class fake_queue:
    def get(self):
        return np.ones([500,500])
dummy_queue = fake_queue()

try:
    while True:
        record_image_data(dummy_queue)
        time.sleep(.5)

except KeyboardInterrupt:
    save_image_data()
    exit(9)
