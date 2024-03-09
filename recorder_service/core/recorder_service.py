from .storage import Storage, Metadata, RecordID
from .video_source import VideoSource


class RecorderService:
    """
    Core service for capturing video frames and storing them
    """
    storage_service: Storage
    num_frames_to_capture: int
    video_source: VideoSource

    def __init__(self, num_frames_to_capture: int, video_source: VideoSource, storage_service: Storage):
        """
        :param num_frames_to_capture: Number of frames to capture on each trigger
        :param video_source: Source of video frames
        :param storage_service: Storage backend to store captured frames and metadata
        """
        self.num_frames_to_capture = num_frames_to_capture
        self.video_source = video_source
        self.storage_service = storage_service

    def trigger_video_capture(self, metadata: Metadata) -> RecordID:
        """
        Triggers video recording and stores the frames and metadata
        :param metadata: Arbitrary metadata to store with the video frames
        :return: ID of the stored video record that can be used to retrieve the video frames later
        """
        video_frames = self.video_source.capture_last_frames(self.num_frames_to_capture)
        return self.storage_service.store_video_record(video_frames, metadata)
