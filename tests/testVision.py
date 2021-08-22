import cv2 as cv
import logging
import os
from unittest import TestCase

import settings
from src.cameraVision.exceptions import CameraNotFound
from src.cameraVision.vision import Vision
from time import sleep

logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')


class TestVision(TestCase):
    def test_getFrame(self):
        """In order to turn off overlay pass None insted of filePath.

        """
        image = None
        image = os.path.join(settings.IMAGES_PATH, 'bg_overlay.png')
        vision = Vision(overlayPath=image)
        vision.start()
        while True:
            frame = vision.getFrame()
            if frame is not None:
                cv.imshow("Camera test", frame)

            key = cv.waitKey(10)
            if key & 0xFF == ord('q'):
                logging.info("Quiting")
                cv.destroyAllWindows()
                vision.stop()
                break



    def testGetFrame(self):
        vision = Vision()
        vision.start()
        frame = vision.getFrameForce()
        vision.stop()
        self.assertIsNotNone(frame)

    def testNoCameraFound(self):
        v = Vision(99)
        self.assertRaises(CameraNotFound, v.handleCamera)
        v.stop()

    pass
