"""FYBLOG URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve
from nnblog import settings
from blog import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),


    # 博客首页http://127.0.0.1/
    url(r'^$',views.Main.as_view(),name='main'),

    # 登录页面http://127.0.0.1/login$
    url(r'^login',views.Login.as_view(),name='login'),

    # 登录页面验证码图片请求http://127.0.0.1/get_valid_img
    # url(r'^get_valid_img',views.GetValidImg.as_view(),name='get_valid_img'),

    # 退出登录http://127.0.0.1/logout$
    url(r'^logout$', views.Logout.as_view(), name='logout'),

    url(r'^agreement$', views.agreement, name='agreement'),

    # 注册http://127.0.0.1/register$
    url(r'^register$',views.Register.as_view(),name='register'),

    # 注册时ajax验证
    url(r'^reg_valid$',views.RegisterValid.as_view(),name='reg_valid'),


    # 查看有密码的博客时验证密码
    url(r'^article_pwd_valid', views.ArticlePwdValid.as_view(), name='article_pwd_valid'),
    # url(r'pwd', views.ArticlePwdValid.as_view(), name='xxx'),


    # 博客详情页http://127.0.0.1/fuyong/article/1688.html
    url(r'^(?P<bottom_url>\w+)/article/(?P<article_id>\d+).html',views.ArticleDetail.as_view(),name='article_detail'),


    # 博客点赞踩灭  ajax提交
    url(r'^article/poll$',views.ArticlePoll.as_view(),name='article_poll'),

    # 发表博客评论，ajanx提交
    url(r'^post_comment/(?P<pid>\d*)$', views.CommentPost.as_view(), name='post_comment'),

    # 博客的增删改以及置顶http://127.0.0.1/manage/article/add 或 http://127.0.0.1/manage/article/delete/2
    url(r'^manage/article/(?P<handle>add|update|delete|stick|password|drafts)/(?P<article_id>\d*)$', views.ArticleManage.as_view(), name='article_manage'),

    # 发布草稿箱里的博客
    url(r'^post_drafts_blog', views.PostDraftsBlog.as_view(), name='post_drafts_blog'),

    # 博客分类的增删改以及置顶http://127.0.0.1/manage/category/add 或 http://127.0.0.1/manage/category/delete/2
    url(r'^manage/category/(?P<handle>add|update|delete)/(?P<category_id>\d*)$', views.CategoryManage.as_view(), name='category_manage'),

    # 友情链接的增删改以及置顶http://127.0.0.1/manage/friendlylink/add 或 http://127.0.0.1/manage/friendlylink/delete/2
    url(r'^manage/friendlylink/(?P<handle>add|update|delete)/(?P<link_id>\d*)$', views.FriendlylinkManage.as_view(), name='friendlylink_manage'),


    # 后台管理首页
    # url(r'^i$', views.Manage.as_view(), name='i'),

    # 后台管理http://127.0.0.1/manage/article
    url(r'^manage/(article|drafts|category|friendlylink|user)$', views.Manage.as_view(), name='manage'),

    # 用户信息更改http://127.0.0.1/userinfo/update/avatar
    url(r'^userinfo/update/(\w+)', views.UserInfoUpdate.as_view(), name='user_info_update'),

    # media文件路径设置
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    # 分类、标签、时间归档、搜索等页面 127.0.0.1/fuyong/articles/category/python  或 127.0.0.1/fuyong/articles/archive/2015-8-8
    url(r'^(?P<bottom_url>\w+)/articles/(?P<view>category|archive|search)/(?P<condition>.*)$', views.HomeSite.as_view(), name='articles'),

    # 登陆时滑动验证
    url(r'^pc-geetest/register', views.pcgetcaptcha, name='pcgetcaptcha'),

    # # 个人博客首页http://127.0.0.1/
    url(r'^(?P<bottom_url>\w+)$',views.HomeSite.as_view(),name='home_site')

]

