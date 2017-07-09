from django import template
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

register=template.Library()

@register.simple_tag(takes_context=True)
def paginate(context,objects_list,pages_count):
    left=3
    right=3
    paginator=Paginator(objects_list,pages_count)
    page=context['request'].GET.get('page')

    try:
        objects_list=paginator.page(page)
        context['current_page']=int(page)
        pages=get_left(context['current_page'],left,paginator.num_pages)+get_right(context['current_page'],right,paginator.num_pages)
    except PageNotAnInteger:
        objects_list=paginator.page(1)
        context['current_page']=1
        #由于是第一页，所以只有右边有页码，而左边没有
        pages=get_right(context['current_page'],right,paginator.num_pages)
    except EmptyPage:
        objects_list=paginator.page(paginator.num_pages)
        context['current_page']=paginator.num_pages
        pages=get_left(context['current_page'],left,paginator.num_pages)

    context['post_list']=objects_list
    context['pages']=pages
    context['last_page']=paginator.num_pages
    context['first_page']=1

    try:
        context['pages_first']=pages[0]
        context['pages_last']=pages[-1]+1
    except IndexError:
        context['pages_first']=1
        context['pages_last']=2
    return ' '

#获得当前页面左边页码的方法
def get_left(current_page,left,num_pages):
    if current_page==1:
        return []
    elif current_page==num_pages:
        l=[i-1 for i in range(current_page,current_page-left,-1) if i-1>1]
        l.sort()
        return l
    l=[i for i in range(current_page,current_page-left,-1) if i>1]
    l.sort()
    return l

def get_right(current_page,right,num_pages):
    if current_page==num_pages:
        return[]
    return[i+1 for i in range(current_page,current_page+right-1) if i<num_pages-1]




