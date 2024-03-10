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
    def store_video_record(
        self, video_frames: list[VideoFrame], metadata: Metadata
    ) -> RecordID:
        """
        Store provided video frames and metadata and return a unique ID for later retrieval
        :param video_frames: frames to store
        :param metadata: metadata to store
        :return: record ID for later retrieval
        """
        pass

    @abc.abstractmethod
    def list_video_records(self) -> list[tuple[RecordID, Metadata]]:
        pass

    @abc.abstractmethod
    def get_video_record(
        self, record_id: RecordID
    ) -> tuple[list[VideoFrame], Metadata]:
        pass

    class RecordNotFoundError(Exception):
        pass
