from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from PIL import Image


# Create your models here.

class Tutorial(models.Model):
    title = models.CharField(max_length=100)
    liked_by = models.ManyToManyField(User,related_name='liked_by_question',blank = True)
    like = models.IntegerField(default=0)
    content = models.TextField()
    date_published = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    image = models.ImageField(upload_to="image",blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tutorial')

class Comment(models.Model):
    post = models.ForeignKey(Tutorial,on_delete=models.CASCADE,related_name="comments")
    liked_by = models.ManyToManyField(User,related_name='liked_by',blank = True)
    like = models.IntegerField(default=0)
    r_token = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_published = models.DateTimeField(default=timezone.now)
    comment = models.TextField()

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('tutorial')

class Qcomment(models.Model):
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="Qcomments")
    liked_by = models.ManyToManyField(User,related_name='liked_by_qcomment',blank = True)
    like = models.IntegerField(default=0)
    r_token = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_published = models.DateTimeField(default=timezone.now)
    qcomment = models.TextField()

    def __str__(self):
        return self.qcomment

    def get_absolute_url(self):
        return reverse('tutorial')

    

class FilesAdmin(models.Model):
	file = models.FileField(upload_to='media')
	title=models.CharField(max_length=50)

	def __str__(self):
		return self.title
