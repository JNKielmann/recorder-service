import os
from pathlib import Path

from recorder_service.core.recorder_service import RecorderService
from recorder_service.video import LocalVideoSource
from recorder_service.storage import LocalFilesystemStorage

# Load configuration from environment variables
local_video_path = Path(os.getenv("LOCAL_VIDEO", default="data/test_video.mp4"))
if not local_video_path.exists():
    raise FileNotFoundError(f"Local video file {local_video_path} does not exist. Ensure environment variable LOCAL_VIDEO is set correctly.")
storage_dir = Path(os.getenv("STORAGE_DIR", default="data/storage"))
num_frames_to_capture = int(os.getenv("NUM_FRAMES_TO_CAPTURE", default=5))

# Set up the recorder service
video_source = LocalVideoSource(local_video_path)
storage_service = LocalFilesystemStorage(storage_dir)
recorder_service = RecorderService(num_frames_to_capture, video_source, storage_service)
