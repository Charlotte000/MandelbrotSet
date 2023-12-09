import cv2
import cv2.typing
from dask.distributed import Client

from Animation import Animation, Camera
from MandelbrotSet import MandelbrotSet
from VideoCreator import VideoCreator


def render(address: str | None, images_folder: str, resolution: tuple[int, int], animation: Animation) -> None:
    client = Client(address)

    if address:
        client.upload_file('Camera.py')
        client.upload_file('MandelbrotSet.py')

    futures = [
        client.submit(
            MandelbrotSet.colorize,
            client.submit(MandelbrotSet.render, resolution, camera), colorizer)
        for camera, colorizer in animation.animate()
    ]

    for index, future in enumerate(futures):
        image: cv2.typing.MatLike = future.result()
        cv2.imwrite(f'{images_folder}/img{index}.png', image)

    client.close()


def main():
    begin = Camera((-1.78, 0), (3, 3), 60)
    end = Camera((-1.78, 0), (.00001, .00001), 200)
    animation = Animation(begin, end, lambda _: MandelbrotSet.hsv, 300)


    import time

    begin = time.perf_counter()
    render('tcp://192.168.1.107:8786', 'imgs', (500, 500), animation)

    end = time.perf_counter()
    print(end - begin)

    # VideoCreator.create('imgs', 'vids/output6.mp4')

    # middle = Camera((-1, 0), (3, 3), 20)
    # cv2.imshow('test.png', MandelbrotSet.render((500, 500), middle, False))
    # cv2.waitKey(0)


if __name__ == '__main__':
    main()
