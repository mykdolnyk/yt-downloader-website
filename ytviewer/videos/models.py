from django.db import models

# Create your models here.
class Video(models.Model):
    ytid = models.TextField('YouTube ID', null=False)
    """Video Youtube ID"""
    title = models.TextField('Video Title', default="A Youtube Video")
    file = models.FileField("Video File", upload_to='videos/', null=False)