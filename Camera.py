from dataclasses import dataclass


@dataclass
class Camera:
    center: tuple[float, float]
    size: tuple[float, float]
    max_iteration: int

    def left_up(self) -> tuple[float, float]:
        return (self.center[0] - self.size[0] / 2, self.center[1] - self.size[1] / 2)
