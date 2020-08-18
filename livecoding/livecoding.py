from threading import Thread, Lock, Event
from collections import defaultdict
from pythonosc import dispatcher, osc_server
from p5 import run

class BaseSession(object):
    """Base class for creating a live coding session
    using OSC and p5 each one looping in a different thread."""

    def __init__(self, lock_method, *args, **kwargs):
        self.lock_method = lock_method
        self.handler = None
        self.address =  '127.0.0.1'
        self.port = 7070
        self.frame_rate = 60
        self.mode = "P2D"
        self.threads = []
        self.parameters = defaultdict(lambda: None)
        self.verbose = 0

        if self.lock_method != None:
            self.lock = Lock()
        else:
            self.lock = None

    def config(self):
        """Session configuration"""
        osc_kwargs={
                "folder": self.folder,
                "handler": self.handler,
                }
        p5_kwargs={"sketch_setup": self.setup,
                "sketch_draw": self.draw,
                "frame_rate": self.frame_rate,
                "mode": self.mode}
        self.threads.append(Thread(
            name="osc", target=self.listen_osc, kwargs=osc_kwargs))
        self.threads.append(Thread(
            name="p5", target=self.run_p5, kwargs=p5_kwargs))

    def listen_osc(self, folder, handler, *args):
        """Listen osc at address, port with handler function forever"""
        dispatcher_ = dispatcher.Dispatcher()
        dispatcher_.map(folder, handler, *args)
        server = osc_server.BlockingOSCUDPServer(
            (self.address, self.port), dispatcher_)
        if self.verbose:
            print(f"Serving on {server.server_address}")
        server.serve_forever()

    def run_p5(self, *args, **kwargs):
        """Initializes p5 sketch"""
        run(*args, **kwargs)

    def setup(self):
        """Setup function for p5"""

    def draw(self):
        """Draw function for p5"""

    def run(self):
        """Run livecoding session"""
        self.config()
        for t in self.threads:
            t.start()

    def stop(self):
        """Stop running threads"""
        for t in self.threads:
            t.join()


class TidalSession(BaseSession):
    """Tidal session with functions for handling tidal structures
    dirtStructure (/play) and superdirtStructure (/play2)"""

    def __init__(self, address="127.0.0.1", port=7070,
            folder="/play2", arglist=None, lock_method="manual",
            frame_rate=60, verbose=0, *args, **kwargs):
        super().__init__(lock_method=lock_method, *args, **kwargs)
        self.address = address
        self.port = port
        self.frame_rate = frame_rate
        self.verbose = verbose
        self.folder = folder
        if folder == "/play2":
            self.handler = self.play2_handler
        elif folder == "/play":
            self.handler = self.play_handler
            if arglist == None:
                arglist = ["sec", "usec", "cps", "s", "offset", "begin", "end", "speed", "pan", "velocity", "vowel", "cutoff", "resonance", "accelerate", "shape", "kriole", "gain", "cut", "delay", "delaytime", "delayfeedback", "crush", "coarse", "hcutoff", "hresonance", "bandf", "bandq", "unit", "loop", "n", "attack", "hold", "release", "orbit", "id"]

    def play_handler(self, addr, arglist, *args):
        """Handles /play unamed OSC folder changing values at global
        object parameters"""
        if self.lock_method != None:
            with self.lock:
                self.unamed_OSC_handler(args, arglist)
        else:
            self.unamed_OSC_handler(args, arglist)

    def play2_handler(self, addr, *args):
        """Handles /play2 OSC folder changing values at global
        object parameters"""
        if self.lock_method != None:
            with self.lock:
                self.named_OSC_handler(args)
        else:
            self.named_OSC_handler(args)

    def named_OSC_handler(self, args):
        """Assign OSC named args to parameters variables"""
        for e, f in zip(args[0::2], args[1::2]):
            if self.verbose:
                print(e, f)
            self.parameters[e] = f

    def unamed_OSC_handler(self, args, arglist):
        """Assign OSC unamed args to parameters variables"""
        for i, e in enumerate(arglist):
            if self.verbose:
                print(e, args[i])
            self.parameters[e] = args[i]





