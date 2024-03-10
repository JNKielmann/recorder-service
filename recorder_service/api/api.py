import io
import zipfile
from datetime import datetime

import cv2
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, Response, JSONResponse
from pydantic import BaseModel

from recorder_service.config import recorder_service
from recorder_service.core import VideoFrame, RecordID, Storage

app = FastAPI()


class VideoCaptureInput(BaseModel):
    customer_id: str
    # trigger_time: datetime


@app.post(
    "/trigger-video-capture",
    description="Trigger video capture and store the video frames and metadata",
)
def trigger_video_capture(metadata: VideoCaptureInput):
    id = recorder_service.trigger_video_capture({
        **metadata.dict(),
        "trigger_time": datetime.now().isoformat()
    })
    return {
        "id": id,
    }


@app.get(
    "/video-record",
    description="List id and metadata of all video records",
)
def list_video_records():
    records = recorder_service.list_video_records()
    return [{"id": id, "metadata": metadata} for id, metadata in records]


@app.get(
    "/video-record/{record_id}/metadata",
    description="Get the metadata of a video record",
)
def get_video_record_metadata(record_id: RecordID):
    try:
        _, metadata = recorder_service.get_video_record(record_id)
    except Storage.RecordNotFoundError as e:
        return {"error": str(e)}, 404
    return {
        "id": record_id,
        "metadata": metadata,
    }


@app.get(
    "/video-record/{record_id}/video-frames",
    description="Download a ZIP file containing the png video frames of the record",
)
def get_video_record_frames(record_id: RecordID):
    try:
        frames, _ = recorder_service.get_video_record(record_id)
    except Storage.RecordNotFoundError as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return Response(content=zip_video_frames(frames), media_type="application/zip", headers={
        "Content-Disposition": f"attachment; filename=video_frames_of_{record_id}.zip"
    })


def zip_video_frames(frames: list[VideoFrame]) -> bytes:
    zip_in_memory = io.BytesIO()
    with zipfile.ZipFile(zip_in_memory, mode="w") as zip_file:
        for i, frame in enumerate(frames):
            frame_bytes = cv2.imencode(".png", frame)[1].tobytes()
            zip_file.writestr(f"frame_{i}.png", frame_bytes)
    return zip_in_memory.getvalue()


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')
