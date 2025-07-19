import os
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from .models import Video
from django.core.files import File
from .helpers import url, video
from yt_dlp import DownloadError

def index_page(request: HttpRequest):
    return render(request, 'videos/index.html', {})


def video_page(request: HttpRequest):
    context = {'errors': []}
    
    # Check if the URL is actually a URL and if it is valid
    video_id = request.GET.get('video_url')
    if url.is_url(video_id):
        try:
            video_id = url.get_video_id(video_id)
        except ValueError:
            context['errors'].append('Something went wrong! Please double-check if the ID/URL you entered is correct.')
            return render(request, 'videos/error_page.html', context)

    video_querylist = Video.objects.filter(ytid=video_id)
    
    if len(video_querylist) == 0:
        # If video was not downloaded before
        
        try:
            video_details = video.download_video(video_id=video_id)
        except DownloadError:
            context['errors'].append('Something went wrong! Please double-check if the ID/URL you entered is correct.')
            return render(request, 'videos/error_page.html', context)

        # Save the file into the Video object
        video_object = Video(ytid=video_id, title=video_details['title'])
        video_object.file.name = video_details['filepath']
        video_object.save()
    else:
        video_object = video_querylist.get()

    context['video'] = video_object
    
    return render(request, 'videos/watch_video.html', context)
