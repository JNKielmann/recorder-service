from recorder_service.core import RecorderService, VideoSource, Storage
from unittest import mock


def test_trigger_video_capture():
    video_source = mock.Mock()
    video_source.capture_last_frames.return_value = ["frame1", "frame2", "frame3"]
    storage = mock.Mock()
    storage.store_video_record.return_value = "test-id"
    recorder_service = RecorderService(3, video_source, storage)

    id = recorder_service.trigger_video_capture({
        "customer_id": "test-customer",
    })

    storage.store_video_record.assert_called_once_with(
        ["frame1", "frame2", "frame3"], {"customer_id": "test-customer", }
    )
    assert id == "test-id"
