from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from .models import Video, VideoStatus
from .helpers import url
from .tasks import download_video_task


def index_page(request: HttpRequest):
    return render(request, 'videos/index.html', {})


def show_video(request: HttpRequest):
    context = {'errors': []}

    # Check if the URL is actually a URL and if it is valid
    video_id = request.GET.get('video_url')
    if url.is_url(video_id):
        try:
            video_id = url.get_video_id(video_id)
        except ValueError:
            context['errors'].append(
                'Something went wrong! Please double-check if the ID/URL you entered is correct.')
            return render(request, 'videos/error_page.html', context)

    video_object = Video.objects.filter(ytid=video_id).last()

    if video_object is None:
        context['errors'].append(
            'Something went wrong! If you entered this link manually, please try doing that from the home page.')
        return render(request, 'videos/error_page.html', context)

    context['video'] = video_object

    return render(request, 'videos/watch_video.html', context)


def queue_video(request: HttpRequest):
    """Starts the video downloading process."""
    # Check if the URL is actually a URL and if it is valid
    video_id = request.GET.get('video_url')
    if url.is_url(video_id):
        try:
            video_id = url.get_video_id(video_id)
        except ValueError:
            return JsonResponse({'success': False,
                                 'errors': ['Something went wrong! Please double-check if the ID/URL you entered is correct.']})

    exists = Video.objects.filter(ytid=video_id).exists()

    if not exists:
        Video.objects.create(ytid=video_id)
        download_video_task.delay(video_id=video_id)

    return JsonResponse({'success': True,
                         'video_id': video_id})


def get_video_details(request: HttpRequest):
    """Checks if the video is ready, and returns the required details if so."""
    video_id = request.GET.get('video_id')
    
    try:
        video_object = Video.objects.get(ytid=video_id)
    except Video.DoesNotExist:
        return JsonResponse({
            'success': False,
            'errors': ['Something went wrong! If you entered this link manually, please try doing that from the home page.']
        })
    
    if video_object.status == VideoStatus.PENDING:
        return JsonResponse({
            'success': True,
            'status': video_object.get_status_display() # Returns status as a string
        })        
    elif video_object.status == VideoStatus.COMPLETE:
        return JsonResponse({
            'success': True,
            'status': video_object.get_status_display(),
            'title': video_object.title,
            'id': video_object.ytid
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': ['Something went wrong! Please double-check if the ID/URL you entered is correct.']
        })
