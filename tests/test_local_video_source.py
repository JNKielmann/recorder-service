import os
from pathlib import Path

import pytest

from recorder_service.video import LocalVideoSource

this_dir = Path(__file__).parent


def test_video_file_not_found():
    video_path = this_dir / "test-data/unknown_video.mp4"
    with pytest.raises(ValueError, match=f"{video_path} does not exist"):
        LocalVideoSource(Path(video_path))


def test_broken_video_file():
    video_path = this_dir / "test-data/broken_video.mp4"
    with pytest.raises(ValueError, match=f"Failed to open {video_path}"):
        LocalVideoSource(Path(video_path))


def test_capture_last_frames():
    video_path = this_dir / "test-data/test_video.mp4"
    video_source = LocalVideoSource(Path(video_path))
    frames = video_source.capture_last_frames(3)
    assert len(frames) == 3
    for frame in frames:
        assert frame.shape == (720, 1280, 3)
