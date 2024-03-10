import json

import numpy as np
import pytest

from recorder_service.storage.local_filesystem_storage import LocalFilesystemStorage
from pathlib import Path

this_dir = Path(__file__).parent


def test_directory_is_created_if_not_existent():
    storage_dir = this_dir / "test-data/unknown_dir"
    if storage_dir.exists():
        storage_dir.rmdir()
    assert not storage_dir.exists()
    LocalFilesystemStorage(storage_dir)
    assert storage_dir.exists()
    storage_dir.rmdir()


def test_fail_if_path_is_not_a_directory():
    storage_dir = this_dir / "test-data/test_video.mp4"
    assert storage_dir.exists()
    assert storage_dir.is_file()
    with pytest.raises(ValueError, match=f"{storage_dir} is not a directory"):
        LocalFilesystemStorage(storage_dir)


def test_store_video_record(tmp_path):
    storage_service = LocalFilesystemStorage(tmp_path)
    empty_image = np.zeros((720, 1280, 3), np.uint8)
    metadata = {"test": "value"}
    record_id = storage_service.store_video_record([empty_image, empty_image], metadata)
    record_dir = tmp_path / record_id
    assert record_dir.exists()
    assert (record_dir / "frame_0.png").exists()
    assert (record_dir / "frame_1.png").exists()
    metadata_file = record_dir / "metadata.json"
    assert metadata_file.exists()
    read_metadata = json.load(metadata_file.open())
    assert read_metadata == metadata
