import threading


class AlreadyRunning(Exception):
    pass


class IntervalNotValid(Exception):
    pass


class SetInterval:
    def __init__(self, func=None, sec=None, args=None):
        if args is None:
            args = []
        self.running = False
        self.func = func
        self.sec = sec
        self.Return = None
        self.args = args
        self.runOnce = None
        self.runOnceArgs = None

        if func is not None and sec is not None:
            self.running = True

            if not callable(func):
                raise TypeError("non-callable object is given")

            if not isinstance(sec, int) and not isinstance(sec, float):
                raise TypeError("A non-numeric object is given")

            self.TIMER = threading.Timer(self.sec, self.loop)
            self.TIMER.start()

    def start(self):
        if self.running:
            raise AlreadyRunning("Tried to run an already run interval")
        if not self.isValid():
            raise IntervalNotValid(
                "The function and/or the " + "interval hasn't provided or invalid."
            )
        self.running = True
        self.TIMER = threading.Timer(self.sec, self.loop)
        self.TIMER.start()

    def stop(self):
        self.running = False

    def isValid(self):
        if not callable(self.func):
            return False

        cond1 = not isinstance(self.sec, int)
        cond2 = not isinstance(self.sec, float)
        return not cond1 or not cond2

    def loop(self):

        if self.running:
            self.TIMER = threading.Timer(self.sec, self.loop)
            self.TIMER.start()
            function_, Args_ = self.func, self.args

            if self.runOnce is not None:
                runOnce, self.runOnce = self.runOnce, None
                result = runOnce(*self.runOnceArgs)
                self.runOnceArgs = None

                if result is False:
                    return

            self.Return = function_(*Args_)

    def change_interval(self, sec):

        cond1 = not isinstance(sec, int)
        cond2 = not isinstance(sec, float)
        if cond1 and cond2:
            raise TypeError("A non-numeric object is given")

        if self.running:
            self.TIMER.cancel()

        self.sec = sec

        if self.running:
            self.TIMER = threading.Timer(self.sec, self.loop)
            self.TIMER.start()

    def change_next_interval(self, sec):

        if isinstance(sec, (int, float)):
            self.sec = sec
        else:
            raise TypeError("A non-numeric object is given")

    def change_func(self, func, args=None):

        if args is None:
            args = []
        if not callable(func):
            raise TypeError("non-callable object is given")

        self.func = func
        self.args = args

    def run_once(self, func, args=None):
        if args is None:
            args = []
        self.runOnce = func
        self.runOnceArgs = args

    def get_return(self):
        return self.Return
