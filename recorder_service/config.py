import os
from pathlib import Path

from recorder_service.core.recorder_service import RecorderService
from recorder_service.video import LocalVideoSource
from recorder_service.storage import LocalFilesystemStorage

print("TEST ENV: ", os.getenv("TEST"))

video_source = LocalVideoSource(Path("data/test_video.mp4"))
storage_service = LocalFilesystemStorage(Path("data/storage"))
recorder_service = RecorderService(3, video_source, storage_service)
