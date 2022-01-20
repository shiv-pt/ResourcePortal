from django.db import models

# Create your models here.

class Material(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    type=models.CharField(max_length=100)
    thumbnail=models.ImageField(upload_to='material/thumbnail',blank=True)
    semester=models.CharField(max_length=100,blank=True)
    link=models.CharField(max_length=200,blank=True,null=True)
    document=models.FileField(upload_to='material/document',blank=True,null=True)
    video=models.FileField(upload_to='material/video',blank=True,null=True)
    like_count=models.IntegerField(default=0)
    dislike_count=models.IntegerField(default=0)

    class Meta:
        db_table='material'

    def __str__(self):
        return self.title


