import time
from grove.gpio import GPIO


class GroveCollisionSensor(GPIO):
    def __init__(self, pin):
        super(GroveCollisionSensor, self).__init__(pin, GPIO.IN)
        self._last_time = time.time()

        self._on_collision = None
        self._on_NoCollision = None
        self.collisionState = False

    @property
    def on_collision(self):
        return self._on_collision

    @on_collision.setter
    def on_collision(self, callback):
        if not callable(callback):
            return

        if self.on_event is None:
            self.on_event = self._handle_event

        self._on_collision = callback

    @property
    def on_NoCollision(self):
        return self._on_NoCollision

    @on_NoCollision.setter
    def on_NoCollision(self, callback):
        if not callable(callback):
            return

        if self.on_event is None:
            self.on_event = self._handle_event

        self._on_NoCollision = callback

    def _handle_event(self, pin, value):
        t = time.time()
        dt, self._last_time = t - self._last_time, t

        if not value:
            if callable(self._on_collision):
                self._on_collision(dt)
        else:
            if callable(self._on_NoCollision):
                self._on_NoCollision(dt)


Grove = GroveCollisionSensor


def main():
    import sys

    if len(sys.argv) < 2:
        print('Usage: {} pin'.format(sys.argv[0]))
        sys.exit(1)

    button = GroveCollisionSensor(int(sys.argv[1]))

    def on_collision(t):
        print('Collision')

    def on_NoCollision(t):
        print("No Collision")

    button.on_collision = on_collision
    # button.on_NoCollision = on_NoCollision

    while True:
        time.sleep(1)