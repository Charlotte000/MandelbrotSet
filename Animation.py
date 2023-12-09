import math
from dataclasses import dataclass
from typing import Callable, Generator

from Camera import Camera
from MandelbrotSet import Colorizer


@dataclass
class Animation:
    begin: Camera
    end: Camera
    colorizer_generator: Callable[[float], Colorizer]
    frames: int

    def animate(self) -> Generator[tuple[Camera, Colorizer], None, None]:
        if self.frames <= 1:
            yield (self.end, self.colorizer_generator(1))
            return

        for i in range(self.frames):
            time = i / (self.frames - 1)
            yield (
                Camera(
                    (Animation.lerp(self.begin.center[0], self.end.center[0], time), Animation.lerp(
                        self.begin.center[1], self.end.center[1], time)),
                    (Animation.exp(self.begin.size[0], self.end.size[0], time), Animation.exp(
                        self.begin.size[1], self.end.size[1], time)),
                    int(Animation.lerp(self.begin.max_iteration,
                        self.end.max_iteration, time))
                ),
                self.colorizer_generator(time)
            )

    @staticmethod
    def lerp(start: float, end: float, t: float) -> float:
        return start * (1 - t) + end * t

    @staticmethod
    def exp(start: float, end: float, t: float) -> float:
        return math.pow(start, 1 - t) * math.pow(end, t)
