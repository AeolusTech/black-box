#!/usr/bin/env python3
import sys
import time
from grove.gpio import GPIO
from zeroless import Server


class __GroveCollisionSensor__(GPIO):
    def __init__(self, pin):
        super(__GroveCollisionSensor__, self).__init__(pin, GPIO.IN)
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


class CollisionSensor():

    keeprunning = True
    # conected to A1 so type 1 as a parameter
    button = __GroveCollisionSensor__(1)
    data = 0

    def on_collision(self, t):
        self.data = 1

    def on_NoCollision(self, t):
        self.data = 0

    def __init__(self):
        self.button.on_collision = self.on_collision
        self.button.on_NoCollision = self.on_NoCollision

        self.publisher = Server(port=12355).pub(
            topic=b'collision_sensor', embed_topic=True)

        time.sleep(1)

    def stop(self):
        self.keeprunning = False

    def run(self):
        while self.keeprunning:
            self.publisher(str(self.data).encode())

            time.sleep(1)
