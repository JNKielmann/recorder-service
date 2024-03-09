from pathlib import Path

from recorder_service.core.recorder_service import RecorderService
from recorder_service.video import LocalVideoSource
from recorder_service.storage import LocalFilesystemStorage

video_source = LocalVideoSource()
storage_service = LocalFilesystemStorage()
recorder_service = RecorderService(3, video_source, storage_service)
