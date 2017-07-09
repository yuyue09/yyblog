from django import template
from ..models import Post,Category

register=template.Library()

#最近文章列表
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all()[:num]

#归档
@register.simple_tag
def archives():
    return Post.objects.dates('create_time','month',order='DESC')

#分类
@register.simple_tag
def categories():
    return Category.objects.all()

#分类及对应文章列表
@register.simple_tag
def get_categories():
    category_list=Category.objects.all()
    #用来装类型和类型对应文章列表
    cate_posts=[]
    for category in category_list:
        categories=[]
        #类型对应的文章结果集
        cate_posts_num=Post.objects.filter(category=category)
        categories.append(category)
        categories.append(cate_posts_num)
        cate_posts.append(categories)
    return cate_posts



