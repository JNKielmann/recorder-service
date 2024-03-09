import abc
import typing

VideoFrame: typing.TypeAlias = str


class VideoSource(abc.ABC):
    @abc.abstractmethod
    def capture_last_frames(self, num_frames: int) -> list[VideoFrame]:
        pass
