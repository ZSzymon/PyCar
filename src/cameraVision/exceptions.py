
class CameraException(Exception):
    """Base camera exception"""

class CameraNotFound(CameraException):
    """Camera not found."""
