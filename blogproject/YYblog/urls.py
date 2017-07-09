from . import views
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

app_name='YYblog'
urlpatterns=[url(r'^$', views.index, name='index'),
                     url(r'^regist/$', views.UserForm.regist, name='regist'),
                     #url(r'^activate/(?P<token>b\'[A-Za-z0-9-._]+)\'$',views.active_user,name='active_user'),
                     url(r'^login/$', views.LoginForm.login, name='login'),
                     url(r'^logout/$',views.logout_user,name='logout'),
                     url(r'^blog/$',views.BlogForm.blog,name='blog'),
                     url(r'^editblog/(?P<post_id>[0-9]+)$',views.editBlog,name='editblog'),
                     url(r'^activities/(?P<user_id>[0-9]+)$',views.activities,name='activities'),
                     url(r'^messages/(?P<user_id>[0-9]+)$',views.owner_message,name='owner_message'),
                     #添加个人资料
                     url(r'^editmessage/$',views.editMessage,name='editMessage'),
                     #更新个人资料
                     url(r'^updatemessage/$',views.updateMessage,name='updateMessage'),
                     url(r'^collects/(?P<user_id>[0-9]+)$',views.collects,name='collects'),
                     url(r'^follows/(?P<user_id>[0-9]+)$',views.follows,name='follows'),
                     url(r'^post/(?P<pk>[0-9]+)$', views.detail, name='detail'),
                     url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
                    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
                    url(r'^collect/(?P<post_id>[0-9]+)$',views.collect,name='collect'),
                    url(r'^uncollect/(?P<post_id>[0-9]+)$',views.uncollect,name='uncollect'),
                    url(r'^follow/(?P<user_id>[0-9]+)$',views.follow,name='follow'),
                    url(r'^unfollow/(?P<user_id>[0-9]+)$',views.unfollow,name='unfollow'),
                    url(r'^test/$', views.test, name='test'),
                    #点赞文章
                    url(r'^like/(?P<post_id>[0-9]+)$',views.like,name='like'),
                    url(r'^unlike/(?P<post_id>[0-9]+)$',views.unlike,name='unlike'),
                     url(r'^home/(?P<pk>[0-9]+)/$', views.home, name='home'),
                                            ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)