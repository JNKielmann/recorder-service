import io
import os
import shutil
import zipfile
from pathlib import Path

import cv2
import numpy as np
from fastapi.testclient import TestClient

this_dir = Path(__file__).parent
os.environ["LOCAL_VIDEO"] = str(this_dir / "test-data/test_video.mp4")
storage_dir = this_dir / "test-data/e2e-storage"
os.environ["STORAGE_DIR"] = str(storage_dir)
os.environ["NUM_FRAMES_TO_CAPTURE"] = "2"

from recorder_service.api import app


def test_trigger_video_capture_and_request_result():
    shutil.rmtree(str(storage_dir))
    storage_dir.mkdir()
    client = TestClient(app)

    record_id = trigger_video_capture(client)

    body = list_video_records(client)
    assert len(body) == 1
    assert body[0]["id"] == record_id

    metadata = get_video_record_metadata(client, record_id)
    assert metadata["customer_id"] == "test-customer"

    frames = get_video_record_frames(client, record_id)
    assert len(frames) == 2
    assert all(frame.shape == (720, 1280, 3) for frame in frames)
    assert not np.array_equal(frames[0], frames[1])


def get_video_record_frames(client, record_id) -> list[cv2.typing.MatLike]:
    response = client.get(f"/video-record/{record_id}/video-frames")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"
    with zipfile.ZipFile(io.BytesIO(response.content), mode="r") as zip_file:
        frames = []
        for file in zip_file.namelist():
            frame_bytes = zip_file.read(file)
            frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)
            frames.append(frame)
    return frames


def trigger_video_capture(client) -> str:
    response = client.post("/trigger-video-capture", json={
        "customer_id": "test-customer",
    })
    assert response.status_code == 200
    body = response.json()
    assert "id" in body
    return body["id"]


def list_video_records(client) -> list[dict]:
    response = client.get("/video-record")
    assert response.status_code == 200
    return response.json()


def get_video_record_metadata(client, record_id) -> dict:
    response = client.get(f"/video-record/{record_id}/metadata")
    assert response.status_code == 200
    body = response.json()
    assert "metadata" in body
    return body["metadata"]
