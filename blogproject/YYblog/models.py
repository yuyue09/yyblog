import datetime
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible

# Create your models here.
#建立分类模型
#装饰器用于兼容Python2
@python_2_unicode_compatible
class Category(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

#建立标签模型
@python_2_unicode_compatible
class Tag(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

#建立文章类
@python_2_unicode_compatible
class Post(models.Model):
    #标题
    title=models.CharField(max_length=100)
    #正文
    body=RichTextField('正文') # 使用ckeditor中的RichTextField
    #发表时间与最后修改时间
    create_time=models.DateTimeField()
    modified_time=models.DateTimeField()
    #文章摘要，blank=true表示可以不需要
    excerpt=models.CharField(max_length=200,blank=True)
    #分类和标签，与文章分别是一对多和多对多的关系
    category=models.ForeignKey(Category)
    tags=models.ManyToManyField(Tag,blank=True)
    #作者,从Django中导入用户模型User
    author=models.ForeignKey(User)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('YYblog:detail',kwargs={'pk':self.pk})
   
    class Meta:
        ordering=['-create_time']


#文章状态模型
@python_2_unicode_compatible
class StatePost(models.Model):
    user_id=models.IntegerField()
    post_id=models.IntegerField()
    #点赞状态，1为点赞，0为未点赞,默认为0
    like=models.IntegerField(default=0)
    create_time=models.DateTimeField(default=datetime.datetime.now())




#建立文章收藏模型
@python_2_unicode_compatible
class collectPost(models.Model):
    user_id=models.IntegerField()
    post_id=models.IntegerField()
    #文章收藏时间
    collect_time=models.DateTimeField()

    def __str__(self):
        return self.user_id

    class Meta:
        ordering=['-collect_time']

#用户互相关注模型
@python_2_unicode_compatible
class Follow(models.Model):
    #关注者id
    follow_id=models.IntegerField()
    #被关注者id
    followed_id=models.IntegerField()
    #关注时间
    follow_time=models.DateTimeField()

    

    class Meta:
        ordering=['-follow_time']

#用户信息模型
@python_2_unicode_compatible
class Message(models.Model):
    #性别
    sex=models.IntegerField()
    #个性签名
    about_me=models.TextField(blank=True)
    #居住地
    location=models.CharField(max_length=200,blank=True)
    #职业
    job=models.CharField(max_length=200,blank=True)
    #受教育程度
    edcution=models.CharField(max_length=100,blank=True)
    #信息对应的用户
    owner=models.ForeignKey(User)
    #个人图像
    head_photo=models.ImageField(upload_to='head_photos/',default='head_photos/no_image.jpg')

class Article(models.Model):
    '''日志'''
    title = models.CharField(verbose_name='标题', max_length=150, blank=False, null=False)
    content = RichTextField('正文') # 使用ckeditor中的RichTextField







