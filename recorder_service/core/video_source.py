import abc
import typing

import cv2.typing

VideoFrame: typing.TypeAlias = cv2.typing.MatLike


class VideoSource(abc.ABC):
    @abc.abstractmethod
    def capture_last_frames(self, num_frames: int) -> list[VideoFrame]:
        pass
