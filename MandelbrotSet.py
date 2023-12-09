import colorsys
import math
from typing import Callable

import cv2
import cv2.typing
import numpy as np

from Camera import Camera

Colorizer = Callable[[float], np.ndarray]


class MandelbrotSet:
    IN_SET_VALUE: float = 1

    @staticmethod
    def render(resolution: tuple[int, int], camera: Camera, is_smoothed: bool = True) -> cv2.typing.MatLike:
        img = np.zeros((resolution[1], resolution[0]), np.uint8)

        left_up = camera.left_up()

        calculator = MandelbrotSet.__calculate_smoothed if is_smoothed else MandelbrotSet.__calculate
        for j in range(resolution[1]):
            for i in range(resolution[0]):
                x = left_up[0] + i / resolution[0] * camera.size[0]
                y = left_up[1] + j / resolution[1] * camera.size[1]
                value = calculator(complex(x, y), camera.max_iteration)
                img[j, i] = int(value * 255)

        return img

    @staticmethod
    def colorize(image: cv2.typing.MatLike, colorizer: Colorizer) -> cv2.typing.MatLike:
        if colorizer == MandelbrotSet.gray_scale:
            return image

        new_image = np.zeros((image.shape[0], image.shape[1], 3), np.uint8)
        for j in range(image.shape[0]):
            for i in range(image.shape[1]):
                new_image[j, i] = colorizer(image[j, i] / 255)

        return cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)

    @staticmethod
    def gray_scale(value: float) -> np.ndarray:
        value = int(value * 255)
        return np.array((value, value, value))

    @staticmethod
    def hsv(value: float) -> np.ndarray:
        r, g, b = colorsys.hsv_to_rgb(value, 1, 1)
        return np.array((int(r * 255), int(g * 255), int(b * 255)))

    @staticmethod
    def __calculate(c: complex, max_iteration: int) -> float:
        if MandelbrotSet.__optimization(c.real, c.imag):
            return MandelbrotSet.IN_SET_VALUE

        z = complex(0, 0)
        for i in range(max_iteration + 1):
            z = z * z + c

            # Bail-out
            z_len = abs(z)
            if z_len >= 2:
                return i / max_iteration

        return MandelbrotSet.IN_SET_VALUE

    @staticmethod
    def __calculate_smoothed(c: complex, max_iteration: int) -> float:
        if MandelbrotSet.__optimization(c.real, c.imag):
            return MandelbrotSet.IN_SET_VALUE

        z = complex(0, 0)
        for i in range(max_iteration + 1):
            z = z * z + c

            # Bail-out
            z_len = abs(z)
            if z_len >= 2:
                return (i + 1 - math.log(math.log2(z_len))) / max_iteration

        return MandelbrotSet.IN_SET_VALUE

    @staticmethod
    def __optimization(x: float, y: float) -> bool:
        if -.65 <= y <= .65 and -.75 <= x <= .375:
            # Main cardioid
            p_sq = (x - .25) ** 2 + y ** 2
            p = math.sqrt(p_sq)
            return x <= p - 2 * p_sq + .25

        if -0.25 <= y <= 0.25 and -1.25 <= x <= -.75:
            # Bulb
            return (x + 1) ** 2 + y ** 2 <= .0625

        return False
