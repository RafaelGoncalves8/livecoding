from livecoding import TidalSession
from p5 import *

class MyLiveCodingSession(TidalSession):

    def setup(self):
        size(640, 360)
        background(255)

    def draw(self):
        with self.lock:
            if self.parameters['s'] == 'bd':
                background(255, 50, 50)
            elif self.parameters['s'] == 'sn':
                background(50, 50, 255)

lc = MyLiveCodingSession(verbose=1)
lc.run()
