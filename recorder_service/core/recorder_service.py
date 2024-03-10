from .storage import Storage, Metadata, RecordID
from .video_source import VideoSource, VideoFrame


class RecorderService:
    """
    Core service for capturing video frames and storing them
    """
    storage: Storage
    num_frames_to_capture: int
    video_source: VideoSource

    def __init__(self, num_frames_to_capture: int, video_source: VideoSource, storage: Storage):
        """
        :param num_frames_to_capture: Number of frames to capture on each trigger
        :param video_source: Source of video frames
        :param storage: Storage backend to store captured frames and metadata
        """
        self.num_frames_to_capture = num_frames_to_capture
        self.video_source = video_source
        self.storage = storage

    def trigger_video_capture(self, metadata: Metadata) -> RecordID:
        """
        Triggers video recording and stores the frames and metadata
        :param metadata: Arbitrary metadata to store with the video frames
        :return: ID of the stored video record that can be used to retrieve the video frames later
        """
        video_frames = self.video_source.capture_last_frames(self.num_frames_to_capture)
        return self.storage.store_video_record(video_frames, metadata)

    def list_video_records(self) -> list[tuple[RecordID, Metadata]]:
        return self.storage.list_video_records()

    def get_video_record(self, record_id: RecordID) -> tuple[list[VideoFrame], Metadata]:
        return self.storage.get_video_record(record_id)
