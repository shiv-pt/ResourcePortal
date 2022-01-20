from unicodedata import category
from django.db import models

from material.models import Material
from django.utils.timezone import now

# Create your models here.

class Member(models.Model):
    usn=models.CharField(max_length=100,primary_key=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    material=models.ManyToManyField(Material)
    likes=models.ManyToManyField(Material,related_name='likes')
    dislikes=models.ManyToManyField(Material,related_name='dislikes')
    report=models.ManyToManyField(Material,related_name='report')

    class Meta:
        db_table='member'

    def __str__(self):
        return self.usn

class issues(models.Model):
    issue_id=models.AutoField(primary_key=True)
    category=models.CharField(max_length=100)
    desc=models.TextField(blank=True)
    issue_status=models.CharField(max_length=100,blank=True)
    time_s = models.DateTimeField(default=now, blank=True, null=True)
    usn=models.ForeignKey(Member,on_delete=models.CASCADE)
    class Meta:
        db_table='issues'
    def __str__(self):
        return self.category

class notification(models.Model):
    notification_id=models.AutoField(primary_key=True)
    notification_type=models.CharField(max_length=100)
    notification_desc=models.TextField(blank=True)
    usn=models.ForeignKey(Member,on_delete=models.CASCADE)
    class Meta:
        db_table='notification'
    def __str__(self):
        return self.notification_type


