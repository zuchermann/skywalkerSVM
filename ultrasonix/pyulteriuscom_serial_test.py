# pyulteriuscom_serial_test.py
'''
@author: Bernie Shieh (bshieh@gatech.edu)
'''
import numpy as np
import scipy as sp
#import matplotlib
#matplotlib.use('Agg')
from matplotlib import pyplot as plt
plt.switch_backend('QT5Agg')
plt.ioff()
import time
import Queue
from threading import Thread, Timer
from multiprocessing import Process

from pyulteriuscom import Ulterius, uData, imagingMode

#def init():
    
ult = Ulterius()

print 'Connected: ', ult.connect('128.61.141.122')

ult.freeze()
print 'Freeze State: ', ult.getFreezeState()
print 'Frame count: ', ult.getFrameCount()

ult.selectProbe(0);
ult.selectMode(imagingMode.BMode);
ult.setDataToAcquire(uData.udtRF);
#    ult.setdataReductionRate()

ult.freeze()
print 'Freeze State: ', ult.getFreezeState()
print 'Frame count: ', ult.getFrameCount()

#ult.setFrameCallback(ult._default_frame_callback)
#    return ult
    
#def run(ult, timeout=10):
#    
#    fig = plt.figure()
#    ax = fig.add_subplot(111)
#    
#    _, desc = ult.getDataDescriptor(uData.udtRF)
#    w, h = desc[1], desc[2]
#    
#    im = ax.imshow(np.zeros((w, h)))
#    fig.canvas.draw()
#    
#    ult.unfreeze()
#
#    time_end = time.time() + timeout
#    while time.time() < time_end:
#        
#        try:
#            frmno, typ, image = ult.getNextFrame(block=False)
#            ax.set_title(str(frmno))
#            im.set_data(image)
#            im.autoscale()
#            fig.canvas.draw()
#            time.sleep(0.1)
#        except Queue.Empty:
#            print 'No frame available!'
#        
#    ult.freeze()
    
def update_plot((w, h), queue):
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    im = ax.imshow(np.zeros((w, h)))
    fig.canvas.draw()
    fig.show()
#    plt.show(block=False)
    
#    while 1:
#        time.sleep(1)
#    time.sleep(20)
#        try:
    
    time_end = time.time() + 20
    while time.time() < time_end:
        
#        frmno, typ, image = ult.getNextFrame(block=True)
        frmno, typ, image = queue.get()
        ax.set_title(str(frmno))
        im.set_data(image)
        im.autoscale()
        fig.canvas.draw()
#        time.sleep(1)
#        except Queue.Empty:
#            print 'No frame available!'
        
#def main():
#    
#    ult = init()
#    run(ult, timeout=10)
#    return ult
    
#def stop():

#    ult.freeze()
#    print 'Freeze state: ', ult.getFreezeState()
#    print ult.frame_queue.qsize()  
    
if __name__ == '__main__':
    
    _, desc = ult.getDataDescriptor(uData.udtRF)
    w, h = desc[1], desc[2]
    
#    thr = Thread(target=update_plot, args=((w,h),))
#    thr.start()
#    p = Process(target=update_plot, args=((w,h), ult.frame_queue))
#    p.start()
    
#    timeout = 10
#    print ult.frame_queue.qsize()
    
#    t = Timer(5, stop)
    
#    ult.unfreeze()
#    t.start()
    
#    time_end = time.time() + timeout
#    while time.time() < time_end:
#        time.sleep(1)
    
#    ult.freeze()
#    print 'Freeze State: ', ult.getFreezeState()
#    print ult.frame_queue.qsize()
