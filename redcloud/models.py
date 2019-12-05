from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import Image
from .validators import image_validator
from django.core.exceptions import ValidationError
import os

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, blank=True, related_name= 'post_likes' )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank = True, null=True, upload_to='post_pics', validators=[image_validator])
    uploaded_file = models.FileField(blank = True, null=True, upload_to='posted_file', default=None)
    tags = TaggableManager( blank=True )


    def __str__(self):
        return ('{} by {}'.format(self.title, self.author))

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    def get_follow_url(self):
        return reverse('post-profile', kwargs={'pk': self.pk})
    def get_like_url(self):
        return reverse('post-like', kwargs={'pk': self.pk})

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 450 or img.width > 450:
            output_size = (450, 450)
            img.thumbnail(output_size)
            img.save(self.image.path)



    class Meta:
        ordering = ('-date_posted',)

class Comment(models.Model):
    commentor = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=200)
    date_commented = models.DateTimeField(auto_now_add= True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-date_commented',)

    def __str__(self):
        #return ('comment on post:  \'{}\' by {}'.format(self.post.title, self.commentor.username))
        return (f'{self.text} commented on {self.post.title}')






"""FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    YEAR_IN_SCHOOL_CHOICES = [
    (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
    ]
    title = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES, default=FRESHMAN,)"""