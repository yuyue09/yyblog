import markdown
import datetime
import os
from PIL import Image
from django import forms
from django.conf import settings as django_settings 
from django.core.mail import send_mail
from . forms import MessageForm
from django.http import HttpResponse,HttpResponseRedirect
from . models import Category,Tag,Post,collectPost,Follow,Message,StatePost
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from comments.forms import CommentForm
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,get_object_or_404,render_to_response,redirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.urlresolvers import reverse

# Create your views here.
#普通用户注册与登录的视图

class UserForm(forms.Form):
    username=forms.CharField(label='用户名', max_length=50)
    password1=forms.CharField(label='密码', widget=forms.PasswordInput())
    password2=forms.CharField(label='确认密码', widget=forms.PasswordInput())
    email=forms.EmailField(label='邮箱')

    def regist(request):
        if request.method=='POST':
            userform=UserForm(request.POST)
            if userform.is_valid():
                username=userform.cleaned_data['username']
                password1=userform.cleaned_data['password1']
                password2=userform.cleaned_data['password2']
                email=userform.cleaned_data['email']
                if password1==password2:
                    user=User.objects.create_user(username=username,password=password1,email=email)
                    user.save()
                    return HttpResponseRedirect(reverse('YYblog:regist'),messages.success(request,'注册成功！'))
                else:
                    messages.error(request,'两次密码必须一致！')
            else:
                messages.error(request,'系统繁忙，请稍后尝试！')
        else:
            userform=UserForm()
        return render(request,'YYblog/regist.html',context={
                      'userform':userform
            })

class LoginForm(forms.Form):
    username=forms.CharField(label='用户名', max_length=50)
    password=forms.CharField(label='密码', widget=forms.PasswordInput())
    
    def login(request):
        if request.method=='POST':
            loginform=LoginForm(request.POST)
            if loginform.is_valid():
                username=loginform.cleaned_data['username']
                password=loginform.cleaned_data['password']
                                                                        #精确等于
                user=authenticate(username=username,password=password)
                

                if user is not None:
                    if user.is_active:
                        login(request,user)
                        return HttpResponseRedirect(reverse('YYblog:index'))
                    else:
                        messages.error(request,'未认证的用户！')
                else:
                    messages.error(request,'用户名或密码错误，请重新登录！')
        else:
            loginform=LoginForm()
        return render(request,'YYblog/login.html',context={'loginform':loginform})

#用户注销
@login_required()
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('YYblog:index'))


#写博客的视图
class BlogForm(forms.Form):
    title=forms.CharField(label='标题', max_length=100)
    
    @login_required()
    def blog(request):
        if request.method=='POST':
            blogform=BlogForm(request.POST)
            if blogform.is_valid():
                author=request.user
                body=request.POST['area']
                title=blogform.cleaned_data['title']
                category=Category.objects.get(name__exact=request.POST['cate'])
               
                if len(body)>20:
                    excerpt=body[0:20]+'...'
                else:
                    excerpt=body+'...'
                create_time=datetime.datetime.now()
                modified_time=datetime.datetime.now()
                post=Post.objects.create(title=title,body=body,excerpt=excerpt,author=author,category=category,create_time=create_time,modified_time=modified_time)
                post.save()
                return HttpResponseRedirect(reverse('YYblog:blog'),messages.success(request,'文章发布成功！'))

        else:
            blogform=BlogForm()
        return render(request,'YYblog/blog.html',context={'blogform':blogform})

@login_required()
def editBlog(request,post_id):
    old_post=Post.objects.filter(id=post_id).first()
    if request.method== 'POST':
        print(request.method)
        blogform=BlogForm(request.POST)
        if blogform.is_valid():
            old_post.body=request.POST['area']
            old_post.title=blogform.cleaned_data['title']
            old_post.category=Category.objects.get(name__exact=request.POST['cate'])
            old_post.modified_time=datetime.datetime.now()
            old_post.save()
            old_post=Post.objects.filter(id=post_id).first()
            return HttpResponseRedirect(reverse('YYblog:home',args=[old_post.author_id]),messages.success(request,'文章修改成功！'))
        else:
            messages.error(request,'提交失败！')
    else:
        blogform=BlogForm()
        context={'blogform':blogform,'old_post':old_post}
    return render(request,'YYblog/edit_blog.html',context=context)




#通用函数
def commons(request,argue):
    return render(request,'YYblog/common.html',context={'argue':argue})


#首页视图
def index(request):
    post_list=Post.objects.all()
    return render(request,'YYblog/index.html',context={
                                 'post_list':post_list
                                
        })

#文章视图
def detail(request,pk):
    post=get_object_or_404(Post,pk=pk)
    #post.body=markdown.markdown(post.body,extensions=['markdown.extensions.extra',
                                                                                               #'markdown.extensions.codehilite',
                                                                                               #'markdown.extensions.toc'])
    post.body=markdown.markdown(post.body,['codehilite'])
    form=CommentForm()
    #获取文章下的评论
    comment_list=post.comment_set.all()
    #判断文章是否自己所写
    #posts=Post.objects.filter(author=request.user)
    collect=collectPost.objects.filter(user_id=request.user.id,post_id=pk)
    statePost=StatePost.objects.filter(user_id=request.user.id,post_id=pk).first()
    #文章赞的个数
    likeCount=StatePost.objects.filter(post_id=pk,like=1).count()
    context={'post':post,
                'collect':collect,
                'statePost':statePost,
                'likeCount':likeCount,
                   'form':form,
                   'comment_list':comment_list
    }
    return render(request,'YYblog/detail.html',context=context)

#归档视图
def archives(request,year,month):
    post_list=Post.objects.get(create_time__year__exact=year,create_time__month__exact=month)
    return render(request,'YYblog/index.html',context={
                             'post_list':post_list
        })
#分类视图
def category(request,pk):
    cate=get_object_or_404(Category,pk=pk)
    post_list=Post.objects.filter(category=cate)
    return render(request,'YYblog/index.html',context={
                'post_list':post_list
        })

#个人主页视图
@login_required()
def home(request,pk):
    current_user=request.user
    author=get_object_or_404(User,pk=pk)
    posts=Post.objects.filter(author=author)
    follow=Follow.objects.filter(follow_id=current_user.id,followed_id=author.id)
    owner_message=Message.objects.filter(owner=author).first()
    context={'posts':posts,'author':author,'current_user':current_user,'follow':follow,'owner_message':owner_message}
    return render(request,'YYblog/home.html',context=context)

#个人动态视图
@login_required()
def activities(request,user_id):
    current_user=request.user
    author=get_object_or_404(User,pk=user_id)
    follow=Follow.objects.filter(follow_id=current_user.id,followed_id=author.id)
    owner_message=Message.objects.filter(owner=author).first()
    context={'current_user':current_user,'author':author,'follow':follow,'owner_message':owner_message,}
    return render(request,'YYblog/activities.html',context=context)

#个人资料视图
@login_required()
def owner_message(request,user_id):
    current_user=request.user
    author=get_object_or_404(User,pk=user_id)
    follow=Follow.objects.filter(follow_id=current_user.id,followed_id=author.id)
    owner_message=Message.objects.filter(owner=author).first()
    #print(owner_message.head_photo)
    #print(owner_message.sex,owner_message.location,owner_message.job,owner_message.edcution)
    context={'current_user':current_user,'author':author,'owner_message':owner_message,'follow':follow}
    return render(request,'YYblog/message.html',context=context)

#收藏文章
@login_required()
def collect(request,post_id):
    post=get_object_or_404(Post,pk=post_id)
    collect=collectPost.objects.create(user_id=request.user.id,post_id=post_id,collect_time=datetime.datetime.now())
    collect.save()
    return HttpResponseRedirect(reverse('YYblog:detail',args=[post_id]))

#取消收藏
@login_required()
def uncollect(request,post_id):
    post=get_object_or_404(Post,pk=post_id)
    collect=collectPost.objects.filter(user_id=request.user.id,post_id=post_id)
    collect.delete()
    return HttpResponseRedirect(reverse('YYblog:detail',args=[post_id]))

#收藏文章列表
@login_required()
def collects(request,user_id):
    current_user=request.user
    author=get_object_or_404(User,pk=user_id)
    follow=Follow.objects.filter(follow_id=current_user.id,followed_id=author.id)
    owner_message=Message.objects.filter(owner=author).first()
    collect_list=collectPost.objects.filter(user_id=user_id)
    post_list=[]
    for collect in collect_list:
        post=get_object_or_404(Post,pk=collect.post_id)
        post_list.append(post)
    context={'post_list':post_list,'current_user':current_user,'author':author,'follow':follow,'owner_message':owner_message}
    return render(request,'YYblog/collects.html',context=context)
   

#关注他人
@login_required()
def follow(request,user_id):
    author=get_object_or_404(User,pk=user_id)
    follow=Follow.objects.create(follow_id=request.user.id,followed_id=author.id,follow_time=datetime.datetime.now())
    follow.save()
    return HttpResponseRedirect(reverse('YYblog:home',args=[user_id]))

#取消关注
@login_required()
def unfollow(request,user_id):
    follow=Follow.objects.filter(follow_id=request.user.id,followed_id=user_id)
    follow.delete()
    return HttpResponseRedirect(reverse('YYblog:home',args=[user_id]))

#关注列表
@login_required()
def follows(request,user_id):
    current_user=request.user
    author=get_object_or_404(User,pk=user_id)
    follow=Follow.objects.filter(follow_id=request.user.id,followed_id=user_id).first()
    #print(follow.follow_id,follow.followed_id,'------------------------')
    owner_message=Message.objects.filter(owner=author).first()
    follows=Follow.objects.filter(follow_id=user_id)
    followed_list=[]
    for follow in follows:
        follows_list=[]
        followed=get_object_or_404(User,pk=follow.followed_id)
        follows_list.append(followed)
        follows_list.append(follow)
        followed_list.append(follows_list)
    context={'followed_list':followed_list,'current_user':current_user,'author':author,'follow':follow,'owner_message':owner_message}
    return render(request,'YYblog/follows.html',context=context)

#添加个人信息
@login_required()
def editMessage(request):
    if request.method=='POST':
        messageform=MessageForm(request.POST,request.FILES)
        if messageform.is_valid():
            owner=request.user
            head_photo=messageform.cleaned_data['head_photo']
            print('----------------------------------',head_photo)
            sex=request.POST['sex']
            location=messageform.cleaned_data['location']
            job=messageform.cleaned_data['job']
            eduction=messageform.cleaned_data['eduction']
            about_me=request.POST['area']
            #采集上传图片
            photo_copy=Image.open(head_photo)
            photo_copy.thumbnail((100,100))
            photo_copy.save('media/head_photos/user'+str(request.user.id)+'.jpg','PNG')
            print('----------------------------------')
            #head_photo.save('user'+str(request.user.id)+'.jpg','PNG')
            #head_photo=head_photo.replace('\\','/')
            #保留裁剪后的图片
            head_photo='head_photos/user'+str(request.user.id)+'.jpg'
            owner_message=Message.objects.create(sex=sex,about_me=about_me,location=location,job=job,
                                                                                 edcution=eduction,owner=owner,head_photo=head_photo)
            owner_message.save()
            return HttpResponseRedirect(reverse('YYblog:editMessage'),messages.success(request,"资料已更新！"))
        else:
            messages.error(request,'信息提交失败！')
    else:
        messageform=MessageForm()
        context={'messageform':messageform}
    return render(request,'YYblog/edit_message.html',context=context)


#更新个人信息
@login_required()
def updateMessage(request):
    old_message=Message.objects.filter(owner=request.user).first()
    if request.method=='POST':
        messageform=MessageForm(request.POST,request.FILES)
        if messageform.is_valid():
            old_message.sex=request.POST['sex']
            old_message.location=messageform.cleaned_data['location']
            old_message.job=messageform.cleaned_data['job']
            old_message.eduction=messageform.cleaned_data['eduction']
            old_message.about_me=request.POST['area']
            if messageform.cleaned_data['head_photo'] is not None and not str(old_message.head_photo).endswith('no_image.jpg'):
                #先删除原有图片
                os.remove(os.path.abspath('media/'+str(old_message.head_photo)).replace('\\','/'))
                #再保存新添加的图片
                head_photo=messageform.cleaned_data['head_photo']
                photo_copy=Image.open(head_photo)
                photo_copy.thumbnail((100,100))
                photo_copy.save('media/head_photos/user'+str(request.user.id)+'.jpg','PNG')
                old_message.head_photo='head_photos/user'+str(request.user.id)+'.jpg'
            #old_message.update(sex=sex,about_me=about_me,location=location,job=job,edcution=eduction)
            old_message.save()
            old_message=Message.objects.filter(owner=request.user).first()
            return HttpResponseRedirect(reverse('YYblog:updateMessage'),messages.success(request,"资料已更新！"))
        else:
            messages.error(request,'信息提交失败！')
    else:
        messageform=MessageForm()
        context={'messageform':messageform,'old_message':old_message}
    return render(request,'YYblog/update_message.html',context=context)


#给文章点赞
@login_required()
def like(request,post_id):
    statePost=StatePost.objects.filter(user_id=request.user.id,post_id=post_id).first()
    if statePost is not None:
        statePost.like=1
        statePost.save()
        return HttpResponseRedirect(reverse('YYblog:detail',args=[post_id]))
    else:
        statePost=StatePost.objects.create(user_id=request.user.id,post_id=post_id,like=1)
        statePost.save()
        return HttpResponseRedirect(reverse('YYblog:detail',args=[post_id]))

#取消点赞
@login_required()
def unlike(request,post_id):
    statePost=StatePost.objects.filter(user_id=request.user.id,post_id=post_id).first()
    statePost.like=0
    statePost.save()
    return HttpResponseRedirect(reverse('YYblog:detail',args=[post_id]))



def test(request):
    return render(request,'test.html')






