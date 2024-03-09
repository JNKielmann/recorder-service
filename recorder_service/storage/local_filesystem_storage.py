import json
import uuid
from pathlib import Path

import cv2

from recorder_service.core import Storage, RecordID, VideoFrame, Metadata


class LocalFilesystemStorage(Storage):
    """
    Storage backend that stores video frames and metadata on the local filesystem.
    For each record, a directory is created with the record ID as the name.
    The directory contains the video frames as PNG files and the metadata as a JSON file.
    """
    def __init__(self, storage_dir: Path):
        """
        :param storage_dir: Directory to store video frames and metadata
        """
        if not storage_dir.exists():
            storage_dir.mkdir(parents=True)
        if not storage_dir.is_dir():
            raise ValueError(f"{storage_dir} is not a directory")
        self.storage_dir = storage_dir

    def store_video_record(self, video_frames: list[VideoFrame], metadata: Metadata) -> RecordID:
        record_id = RecordID(str(uuid.uuid4()))
        record_dir = self.storage_dir / record_id
        record_dir.mkdir()
        for i, frame in enumerate(video_frames):
            frame_file = record_dir / f"frame_{i}.png"
            cv2.imwrite(str(frame_file), frame)
        metadata_file = record_dir / "metadata.json"
        metadata_file.write_text(json.dumps(metadata))
        return record_id
