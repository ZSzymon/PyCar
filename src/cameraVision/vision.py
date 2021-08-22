import cv2 as cv
import threading
import settings
import numpy as np
from src.cameraVision import exceptions


class Vision(threading.Thread):
    _cameraId = 0
    _stopped = False
    _frameLock = threading.Lock()
    _frame = None
    _debug = False
    _overlayPicture = None

    def __init__(self, cameraId=0, overlayPath=None, cameraResolution=(480, 640)):
        self._cameraId = cameraId
        super().__init__()
        self._debug = settings.DEBUG

        if overlayPath is not None:
            """Overlay picture must be same resolution as camera. 
            """
            overlayPicture = cv.imread(overlayPath)
            overlayPicture = cv.resize(overlayPicture, (640, 480), interpolation=cv.INTER_AREA)
            self._overlayPicture = overlayPicture
            pass
        self.cameraResolution = cameraResolution

    def resizePicture(self, img, newResolution):
        """Method resizes photo and returns new photo.

        :param newResolution: new resolution for picture.
        :param img: image to resize
        :return: resized photo
        """
        return cv.resize(img, newResolution, interpolation=cv.INTER_AREA)

    @staticmethod
    def addOverlay(background, foreground, x=0, y=0):
        """Use this method in frameLock context.

        :return: Picture with overlay
        """
        alpha = 1
        beta = 1
        dst = cv.addWeighted(background, alpha, foreground, beta, 0.2)

        return dst

    def handleCamera(self):
        cap = cv.VideoCapture(self._cameraId)
        if not cap.isOpened():
            raise exceptions.CameraNotFound

        while not self._stopped:
            ret, frame = cap.read()
            frame = np.array(frame)
            if self._overlayPicture is not None:
                frame = Vision.addOverlay(frame, self._overlayPicture)
            self.setFrame(frame)
        cap.release()
        pass

    def setFrame(self, screenShot):
        with self._frameLock:
            self._frame = screenShot

    def getFrame(self):
        """ Methods return frame atribute. It's possible that frame is None.
            That means handleCamera does not created frame already.


        :return: frame from camer.
        """
        with self._frameLock:
            frame = self._frame

        return frame

    def getFrameForce(self):
        """This method will wait until camera return proper frame.

        :return: frame
        """

        def _getFrame():
            with self._frameLock:
                f = self._frame
            return f

        frame = None
        while frame is None:
            frame = _getFrame()
        return frame

    def run(self):
        self.handleCamera()

    def start(self):
        self._stopped = False
        super(Vision, self).start()

    def stop(self):
        self._stopped = True
