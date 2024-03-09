import json
import uuid
from pathlib import Path

import cv2

from recorder_service.core import StorageService, RecordID, VideoFrame, Metadata


class LocalFilesystemStorage(StorageService):
    def store_video_record(self, video_frames: list[VideoFrame], metadata: Metadata) -> RecordID:
        print(f"Storing video frames {video_frames} with metadata {metadata}")
        return RecordID(str(uuid.uuid4()))
