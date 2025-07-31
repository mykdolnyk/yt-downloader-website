import os
from django.core.management.base import BaseCommand
from videos.models import Video
import datetime
from django.utils import timezone


class Command(BaseCommand):
    help = 'Deletes Video objects and related files that are older than a certain age.'
    
    def add_arguments(self, parser):
        parser.add_argument('--age', default=6, type=int)
        
    def handle(self, *args, **options):
        max_age = options['age']
        
        delete_after_timestamp = timezone.now() - datetime.timedelta(hours=max_age)
        
        videos_to_delete = Video.objects.filter(requested_at__lt=delete_after_timestamp)
        
        deleted_count = 0
        for video in videos_to_delete:
            if video.file and os.path.exists(video.file.path):
                os.remove(video.file.path)
            video.delete()
            deleted_count += 1

        if deleted_count == 0:
            self.stdout.write(self.style.NOTICE(f'There are no videos older than {max_age} hour(s).'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Deleted {deleted_count} video(s) older than {max_age} hour(s).'))
        