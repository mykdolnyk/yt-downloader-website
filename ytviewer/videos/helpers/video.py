import os
from django.conf import settings
import yt_dlp

def download_video(video_id:str) -> dict:
    """Downloads the video and returns information about it."""
    # Define download options
    ydl_options = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'outtmpl': f'ytviewer/media/videos/{video_id}.%(ext)s',
    }

    # Download the video and get the details
    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        video_info = ydl.extract_info(url=f'https://www.youtube.com/watch?v={video_id}', download=True)
        full_video_filepath = ydl.prepare_filename(video_info)
        rel_video_filepath = os.path.relpath(full_video_filepath, settings.MEDIA_ROOT)
    
        video_title = video_info.get('title')
    
    return {
        'success': True,
        'title': video_title,
        'filepath': rel_video_filepath
    }
