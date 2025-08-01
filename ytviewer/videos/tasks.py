from celery import shared_task
from yt_dlp import DownloadError
from .helpers import downloading
from .models import Video, VideoStatus
from logging import getLogger


task_logger = getLogger(__name__)


@shared_task
def download_video_task(video_id: str):
    try:
        video_object = Video.objects.get(ytid=video_id)
    except Exception:
        task_logger.exception(f'An error occured while trying to retrieve the YouTube Video object with {video_id} ID.')
        raise

    try:
        video_details = downloading.download_video(video_id=video_id)
    except DownloadError:
        video_object.status = VideoStatus.FAILED
        video_object.save()
        return video_object.id

    # Save the file into the Video object
    video_object.ytid = video_id
    video_object.title = video_details['title']
    video_object.description = video_details['description']
    video_object.creation_date = video_details['creation_date']
    video_object.view_count = video_details['view_count']
    video_object.like_count = video_details['like_count']
    video_object.availability = video_details['availability']
    video_object.channel = video_details['channel']
    video_object.channel_url = video_details['channel_url']
    video_object.status = VideoStatus.COMPLETE

    video_object.file.name = video_details['filepath']

    video_object.save()

    return video_object.id
