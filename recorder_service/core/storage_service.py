import abc
import typing

from .video_source import VideoFrame

RecordID = typing.NewType("RecordID", str)
Metadata: typing.TypeAlias = dict


class StorageService(abc.ABC):
    @abc.abstractmethod
    def store_video_record(self, video_frames: list[VideoFrame], metadata: Metadata) -> RecordID:
        pass
