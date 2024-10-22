from controller import Camera
import numpy as np

class CameraWrapper():
    def __init__(self,camera:Camera,timestep:int = 32):
        self.camera = camera
        self.camera.enable(timestep)
        self.WIDTH = self.camera.getWidth()
        self.HEIGHT = self.camera.getHeight()
        self.EXPECTED_LENGTH = self.WIDTH*self.HEIGHT
    
    def getImage(self):
        bgraImageByteString = self.camera.getImage()

        # Ensure the input byte string is of the correct length
        assert len(bgraImageByteString) == self.EXPECTED_LENGTH, f"Expected byte string of length {self.EXPECTED_LENGTH}, got {len(bgraImageByteString)}"

        # Convert the byte string into a NumPy array and eeshape the flat array into (height, width, 4)
        image_array = np.frombuffer(bgraImageByteString, dtype=np.uint8).reshape((self.HEIGHT, self.WIDTH, 4))

        return image_array