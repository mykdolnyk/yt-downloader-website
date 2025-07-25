from django.db import models


class VideoStatus(models.IntegerChoices):
    PENDING = (0, 'pending')
    COMPLETE = (1, 'complete')
    FAILED = (2, 'failed')


class Video(models.Model):
    ytid = models.TextField('YouTube ID', null=False, unique=True)
    title = models.TextField('Title', default="A Youtube Video")
    description = models.TextField('Description', default="No Description")

    creation_date = models.DateTimeField('Became Available On', null=True)
    view_count = models.PositiveBigIntegerField('View Count', default=0)
    like_count = models.PositiveBigIntegerField('Like Count', default=0)
    availability = models.TextField('Video Availability', default='public')

    channel = models.TextField('Video\'s Channel', null=True)
    channel_url = models.TextField('URL of the Channel', null=True)
    
    file = models.FileField("Video File", upload_to='videos/', null=True)
    requested_at = models.DateTimeField('Time of Request', auto_now_add=True)
    status = models.SmallIntegerField('Video Status', choices=VideoStatus.choices, default=VideoStatus.PENDING)
    