## pyulteriuscom.py
'''
A Python wrapper around UlteriusCOM.dll with additional convenience functions.
To register dll, module should be run with elevated privileges.
@author: Bernie Shieh (bshieh@gatech.edu)
'''
import numpy as np
import win32com.client
import os
import subprocess

from multiprocessing import Queue
import time

class _UlteriusEvents:
    '''
    Event class definitions.
    '''
    def OnnewFrameEvent(self, im, typ, cine, frmno):
        pass
    
    def OnparamEvent(self, prmid, x, y):
        pass

class Ulterius:
    '''
    Wrapper class.
    '''
    _ulterius = None
    _ulterius_events = None
    
    def __init__(self, path='bin/', frame_queue=None, MAXQSIZE=40):

        # add bin to path
        os.environ['PATH'] = path +';' + os.environ['PATH']
        
        # register UlteriusCOM.dll
        self._register_dll()

        # dispatch and register callback events
        self._ulterius = win32com.client.Dispatch('UlteriusCOM.Server')
        self._ulterius_events = win32com.client.WithEvents(self._ulterius, 
           _UlteriusEvents)
        
        # init frame queue
        if frame_queue is None:
            self.frame_queue = Queue(maxsize=MAXQSIZE)
        else:
            self.frame_queue = frame_queue
        
        # set default frame callback
        self.setFrameCallback(self._default_frame_callback)
        
    def _register_dll(self):
        subprocess.check_output(['regsvr32', '/s', 'UlteriusCOM.dll'])

    def _unregister_dll(self):
        subprocess.check_output(['regsvr32', '/su', 'UlteriusCOM.dll'])

    def __getattr__(self, name):
        return getattr(self._ulterius, name)
    
#    def __dir__(self):
        
#        class_attrs = self.__class__.__dict__.keys()
#        obj_attrs = self.__dict__.keys()
#        ulterius_attrs = [x for x in dir(self._ulterius) if x not in class_attrs
#                          and x not in obj_attrs]
        
#        return class_attrs + obj_attrs + ulterius_attrs
    
    def __del__(self):
        
        # disconnect from machine
        self.freeze()
        self.disconnect()
        
        # unregister dll
        self._unregister_dll()
    
    def _default_frame_callback(self, im, typ, cine, frmno):
        '''
        Default frame callback. Captured frames are placed into a queue. If the
        queue is full, the frame is dropped.
        '''
        frame_queue = self.frame_queue
        
        if cine or (im is None):
            return
        
        if not frame_queue.full():
            frame_queue.put((frmno, typ, np.array(im)))
        
        
    def setFrameCallback(self, f):
        '''
        Set frame callback to a user-defined function f.
        '''
        _UlteriusEvents.OnnewFrameEvent = f
    
    def setParamCallback(self, f):
        '''
        Set parameter callback to a user-defined function f.
        '''
        _UlteriusEvents.OnparamEvent = f
    
    def freeze(self):
        '''
        Freeze machine image acquisition.
        '''
        if not self.getFreezeState():
            self.toggleFreeze()
        
        assert self.getFreezeState()
    
    def unfreeze(self):
        '''
        Unfreeze machine image acquisition.
        '''
        if self.getFreezeState():
            self.toggleFreeze()

        assert not self.getFreezeState()
    
    def getNextFrame(self, block=True, timeout=None):
        '''
        Returns next frame in queue. If block is False, returns immediately, 
        raising queue.Empty exception if no frame is available. If block is
        True, execution is blocked for timeout until next frame is available,
        or indefinitely if timeout is None.
        '''
        return self.frame_queue.get(block, timeout)

    def getFrameCount(self):
        return self.frame_queue.qsize()

class uData:
    
    udtScreen = 0x00000001
    udtBPre = 0x00000002
    udtBPost = 0x00000004
    udtBPost32 = 0x00000008
    udtRF = 0x00000010
    udtMPre = 0x00000020
    udtMPost = 0x00000040
    udtPWRF = 0x00000080
    udtPWSpectrum = 0x00000100
    udtColorRF = 0x00000200
    udtColorCombined = 0x00000400
    udtColorVelocityVariance = 0x00000800
    udtElastoCombined = 0x00002000
    udtElastoOverlay = 0x00004000
    udtElastoPre  = 0x00008000
    udtECG = 0x00010000
    udtPNG = 0x10000000   

class imagingMode:
    
    UnknownMode = -1
    StartMode = 0

    BMode = 0
    MMode = 1
    ColourMode = 2
    PwMode = 3
    TriplexMode = 4
    PanoMode = 5
    DualMode = 6
    QuadMode = 7
    CompoundMode = 8
    DualColourMode = 9
    DualCompoundMode = 10
    CwMode = 11
    ColorSplitMode = 12
    F4DMode = 13
    TriplexCwMode = 14
    ColourMMode = 15
    ElastoMode = 16
    AnatomicalMMode = 17
    ElastoComparativeMode = 18
    VecDopMode = 19
    BiplaneMode = 20
    FibroMode = 21
    Reslice3DMode = 22
    OAMode = 23
    ContrastMode = 24
    OAHexMode = 25
    OAQuadMode = 26

class uDataDesc:
    pass

#if __name__ == '__main__':
    
#    ult = Ulterius()
    
    # test frame callback
#    ult.testCallback()
    
    # test getDataDescriptor
    # test setParamValue/getParamValue