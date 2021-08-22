
from unittest import TestCase
import settings

class TestSettings(TestCase):
    def testBaseDir(self):
        self.assertEqual("/home/zywko/dev/PyCar", settings.BASE_DIR)

    def testImagesPath(self):
        self.assertEqual("/home/zywko/dev/PyCar/src/images", settings.IMAGES_PATH)