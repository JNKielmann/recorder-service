from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from recorder_service.config import recorder_service

app = FastAPI()


class VideoCaptureInput(BaseModel):
    customer_id: str
    # trigger_time: datetime


@app.post("/trigger-video-capture")
def trigger_video_capture(metadata: VideoCaptureInput):
    id = recorder_service.trigger_video_capture({
        **metadata.dict(),
        "trigger_time": datetime.now().isoformat()
    })
    return {
        "id": id,
    }


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')
