from .forms import CommentForm
from . models import Comment
from YYblog.models import Post
from django.shortcuts import render,get_object_or_404,redirect

# Create your views here.
#文章评论的视图
def post_comment(request,post_pk):
    post=get_object_or_404(Post,pk=post_pk)

    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            name=request.user.username
            email=request.user.email
            text=form.cleaned_data['text']
            #comment.save(commit=False)
            comment=Comment.objects.create(name=name,email=email,text=text,post=post)
            comment.save()
            return redirect(post)
        else:
            comment_list=post.comment_set.all()
            context={'post':post,
                           'form':form,
                           'comment_list':comment_list
            }
            return render(request,'YYblog/detail.html',context=context)
    return redirect(post)

