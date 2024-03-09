from .storage_service import StorageService, Metadata, RecordID
from .video_source import VideoSource


class RecorderService:
    storage_service: StorageService
    num_frames_to_capture: int
    video_source: VideoSource

    def __init__(self, num_frames_to_capture: int, video_source: VideoSource, storage_service: StorageService):
        self.num_frames_to_capture = num_frames_to_capture
        self.video_source = video_source
        self.storage_service = storage_service

    def trigger_video_capture(self, metadata: Metadata) -> RecordID:
        video_frames = self.video_source.capture_last_frames(self.num_frames_to_capture)
        return self.storage_service.store_video_record(video_frames, metadata)
