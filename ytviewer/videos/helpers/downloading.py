import os
from django.conf import settings
import yt_dlp
import datetime
from django.utils import timezone
from logging import getLogger


download_logger = getLogger(__name__)


def download_video(video_id:str) -> dict:
    """Downloads the video and returns information about it."""
    # Define download options
    ydl_options = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'outtmpl': f'{settings.MEDIA_ROOT}/videos/{video_id}.%(ext)s',
        'merge_output_format': 'mp4',
        'cookiefile': os.getenv('YTDLP_COOKIEFILE_PATH'),
    }

    try:
        # Download the video and get the details
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            video_info = ydl.extract_info(url=f'https://www.youtube.com/watch?v={video_id}', download=True)
            full_video_filepath = ydl.prepare_filename(video_info)
            rel_video_filepath = os.path.relpath(full_video_filepath, settings.MEDIA_ROOT)
    except Exception:
        download_logger.exception(f'An error occured while trying to download a YouTube video with {video_id} ID.')
        raise
    
    return {
        'success': True,
        'title': video_info.get('title'),
        'description': video_info.get('description'),
        'filepath': rel_video_filepath,
        'creation_date': timezone.make_aware(datetime.datetime.fromtimestamp(video_info.get('timestamp'))),
        'view_count': video_info.get('view_count'),
        'like_count': video_info.get('like_count'),
        'availability': video_info.get('availability'),
        'channel': video_info.get('channel'),
        'channel_url': video_info.get('channel_url'),
    }
