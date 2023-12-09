import os
import re

import cv2


class VideoCreator:
    @staticmethod
    def create(images_folder: str, file_name: str, frame_rate: float = 60) -> None:
        images = VideoCreator.__get_images(images_folder)

        video = cv2.VideoWriter(
            file_name,
            cv2.VideoWriter.fourcc(*'mp4v'), frame_rate, cv2.imread(images[0]).shape[0:2])
        for img in images:
            video.write(cv2.imread(img))

        video.release()

    @staticmethod
    def __get_images(images_folder: str) -> list[str]:
        return sorted(
            [os.path.join(images_folder, f)
             for f in os.listdir(images_folder)
             if re.fullmatch(r'.*\d+\.png', f)],
            key=lambda f: int(re.findall(r'(\d+)\.png', f)[0])
        )
