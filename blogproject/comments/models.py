from django.db import models
from django.utils.six import python_2_unicode_compatible

# Create your models here.
#评论模型
@python_2_unicode_compatible
class Comment(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    url=models.URLField(blank=True)
    text=models.TextField()
    create_time=models.DateTimeField(auto_now_add=True)
    post=models.ForeignKey('YYblog.Post')

    def __str__(self):
        return self.text[:20]
