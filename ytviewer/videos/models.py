from django.db import models


class VideoStatus(models.IntegerChoices):
    PENDING = (0, 'pending')
    COMPLETE = (1, 'complete')
    FAILED = (2, 'failed')


class Video(models.Model):
    ytid = models.CharField('YouTube ID', null=False, unique=True, max_length=16)
    title = models.CharField('Title', default="A Youtube Video", max_length=128)
    description = models.CharField('Description', default="No Description", max_length=5048)

    creation_date = models.DateTimeField('Became Available On', null=True)
    view_count = models.PositiveBigIntegerField('View Count', default=0)
    like_count = models.PositiveBigIntegerField('Like Count', default=0)
    availability = models.CharField('Video Availability', default='public', max_length=16)

    channel = models.CharField('Video\'s Channel', null=True, max_length=64)
    channel_url = models.CharField('URL of the Channel', null=True, max_length=128)
    
    file = models.FileField("Video File", upload_to='videos/', null=True)
    requested_at = models.DateTimeField('Time of Request', auto_now_add=True)
    status = models.SmallIntegerField('Video Status', choices=VideoStatus.choices, default=VideoStatus.PENDING)
    