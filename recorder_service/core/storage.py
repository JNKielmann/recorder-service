import abc
import typing

from .video_source import VideoFrame

RecordID = typing.NewType("RecordID", str)
Metadata: typing.TypeAlias = dict


class Storage(abc.ABC):
    """
    Interface for storing video frames and metadata
    """
    @abc.abstractmethod
    def store_video_record(self, video_frames: list[VideoFrame], metadata: Metadata) -> RecordID:
        """
        Store provided video frames and metadata and return a unique ID for later retrieval
        :param video_frames: frames to store
        :param metadata: metadata to store
        :return: record ID for later retrieval
        """
        pass
