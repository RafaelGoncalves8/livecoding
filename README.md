# livecoding

![License](https://img.shields.io/github/license/rafaelgoncalves8/livecoding)

Python module to integrate [tidalcycles](https://github.com/tidalcycles/Tidal) and [p5](https://github.com/p5py/p5) using [python-osc](https://github.com/attwad/python-osc) for creating audiovisual performances.

## Installation

Just download this repository in root folder and import as a python module. On linux one can download with git with:
```
   git clone https://github.com/RafaelGoncalves8/livecoding
```

## Configuration

In `bootTidal.hs` change this line from:

```haskell
tidal <- startTidal (superdirtTarget {oLatency = 0.1, oAddress = "127.0.0.1", oPort = 57120}) (defaultConfig {cFrameTimespan = 1/20})
```

to:

```haskell
:{
let prosTarget =
      Target {oName = "processing",
              oAddress = "127.0.0.1",
              oPort = 7070,
              oLatency = 0.2,
              oSchedule = Live,
              oWindow = Nothing
             }
:}


:{
tidal <- startStream defaultConfig [(superdirtTarget, [superdirtShape]),
                                (prosTarget, [superdirtShape])
                               ]
:}

```

Then every OSC data sent to Super Dirt is also sent to port 7070 (which the module uses as default for receiving tidal data).

## Example

```python
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

lc = MyLiveCodingSession()
lc.run()
```

In this example, one creates a session by inheriting a class from `TidalSession` and writing the functions for `setup` and `draw` as one would using p5. The variable `self.lock` is a `threading.Lock` used for avoiding race condition. The variable `self.parameters` is a dictionary in which each key is an OSC variable name and each value is its current value.
