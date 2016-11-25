from __future__ import unicode_literals
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from datetime import datetime


# Create your models here.
# Create your models here.
APPROVAL_CHOICES1 = (
    (1, u'News'),
    (2, u'Memories'),
    (3, u'Facts'),
)

APPROVAL_CHOICES = (
    (u'M', u'Male'),
    (u'F', u'Female'),
)

class Family(models.Model):
    familyName = models.CharField(primary_key=True,max_length=20)
    familyPicture = models.ImageField('Family Picture', upload_to='pic_folder/', default='../static/css/images/bg.jpg')
    aboutFamily = models.TextField('About Family')
    numberOfMembers = models.IntegerField(default=0)

    def publish(self):
        self.save()

    def __str__(self):
        return self.familyName


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    family = models.ForeignKey(Family, on_delete=models.CASCADE, default=1)
    title = models.CharField('Title',max_length=200)
    text = models.TextField('Content')
    img = models.ImageField('Image',upload_to='pic_folder/', default='../static/css/images/bg.jpg')
    post_type = models.IntegerField('Post Type',default=1,choices=APPROVAL_CHOICES1)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title



class Profile(models.Model):
    userName = models.ForeignKey('auth.User')
    familyName = models.ForeignKey(Family, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=20)
    phone = models.CharField('Phone Number', max_length=10)
    gender = models.CharField('Gender', max_length=1, choices=APPROVAL_CHOICES)
    picture = models.ImageField('Profile Picture', upload_to='pictures/', default='../static/css/images/bg.jpg')
    dob = models.DateField('Date Of Birth',default=datetime.now, blank=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey('auth.User', related_name="sender")
    reciever = models.ForeignKey('auth.User')
    msg_content = models.TextField('Message')
    created_at =  models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.created_at = timezone.now()
        self.save()

    def __str__(self):
        return self.msg_content