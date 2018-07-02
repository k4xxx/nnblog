from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.contrib import auth
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.db.models import Count
from django.views import View
# from utils.validimg import ValidCodeImg
from utils.myvalid import MyValid
from utils.mypage import Pagination
from blog import models
import os
import re
from django.db import transaction
from django.db.models import Q
from utils.mypage import Pagination
from bs4 import BeautifulSoup
###########################滑动验证##################################
from blog.geetest import GeetestLib
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
mobile_geetest_id = "7c25da6fe21944cfe507d2f9876775a9"
mobile_geetest_key = "f5883f4ee3bd4fa8caec67941de1b903"
def pcgetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)
###########################滑动验证##################################

# 主页

def agreement(request):
    return render(request,'agreement.html')

class Main(View):
    def get(self,request):
        return render(request,'main.html')

# 注册验证
class RegisterValid(View):
    '''注册输入时ajax验证'''
    def post(self,request):
        data = {'state': False, 'msg': None}

        ipu_name = request.POST.get('inp_name')
        ipu_value = request.POST.get('inp_value')

        valid_res = None

        if ipu_name == 'username':
            if models.UserInfo.objects.filter(username=ipu_value).first():
                data['msg'] = '用户名已存在，换一个试试'
                return JsonResponse(data)
            valid_res = MyValid.valid(ipu_value, str_name='用户名', is_loginname=True, max_length=10, less_length=4)
        elif ipu_name == 'password' or ipu_name == 'password2':
            valid_res = MyValid.valid(ipu_value, str_name='密码', is_loginname=True, max_length=16, less_length=8)
        elif ipu_name == 'nickname':
            valid_res = MyValid.valid(ipu_value, str_name='昵称', is_alnum=True, max_length=16, less_length=4)
        elif ipu_name == 'telephone':
            valid_res = MyValid.valid(ipu_value, str_name='电话', is_telephone=True)
        elif ipu_name == 'email':
            valid_res = MyValid.valid(ipu_value, str_name='邮箱', is_email=True)

        if valid_res['state'] == False:
            data['msg'] = '且'.join(valid_res['error_msg'])
            return JsonResponse(data)
        else:
            data['state'] = True
            return JsonResponse(data)

# 注册提交
class Register(View):
    '''注册按钮提交'''
    def get(self, request):
        return render(request, 'register.html')

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        nickname = request.POST.get('nickname')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        agreement = request.POST.get('agreement')

        data = {'state':False,'msg':None}
        if  not (username.strip() and password.strip() and password2.strip() and nickname.strip()):
            data['msg'] = '用户名、密码及昵称不能为空'
            return JsonResponse(data)
        if password != password2:
            data['msg'] = '两次密码输入不一致'
            return JsonResponse(data)
        if not agreement:
            data['msg'] = '请仔细阅读并同意用户协议'
            return JsonResponse(data)

        # 检查数据库里用户名是否已存在
        if models.UserInfo.objects.filter(username=username).first():
            data['msg'] = '用户名已存在，请换一个试试'
            return JsonResponse(data)

        # 校验每一个输入是否符合规则
        username_valid = MyValid.valid(username, str_name='用户名', is_loginname=True, max_length=10, less_length=4)
        password_valid = MyValid.valid(password, str_name='密码', is_loginname=True, max_length=16, less_length=6)
        nickname_valid = MyValid.valid(nickname, str_name='昵称', is_alnum=True, max_length=18, less_length=2)

        # 验证必填项
        for valid_res in [username_valid,password_valid,nickname_valid]:
            if valid_res['state'] == False:
                data['msg'] = '且'.join(valid_res['error_msg'])
                return JsonResponse(data)


        # 验证选填项
        telephone_valid = MyValid.valid(telephone, str_name='电话', is_telephone=True)
        email_valid = MyValid.valid(email, str_name='邮箱', is_email=True)

        for valid_field in ['telephone','email']:
            if eval(valid_field).strip():
                if eval('%s_valid'%valid_field)['state'] == False:
                    data['msg'] = '且'.join(eval('%s_valid'%valid_field)['error_msg'])
                    return JsonResponse(data)

        try:
            with transaction.atomic():
                user = models.UserInfo.objects.create_user(
                    username=username,
                    password=password,
                    nick_name=nickname,
                    telephone=telephone,
                    email=email,
                )
                # 创建一个用户个人站点,站点后缀默认为用户名
                blog = models.Blog.objects.create(bottom_url=username,title='%s的个人站点'%nickname,theme='default.css',)
                user.blog = blog
                user.save()

                data['state'] = True
        except:
            data['msg'] = '注册失败，请重试'
            return JsonResponse(data)

        return JsonResponse(data)

# 登录验证码=
# class GetValidImg(View):
#     def get(self,request):
#         obj = ValidCodeImg()
#         img_data,valid_code = obj.getValidCodeImg()
#         request.session['valid_code'] = valid_code
#         return HttpResponse(img_data)

# 登录提交
class Login(View):
    def get(self,request):
        return render(request, 'login.html')

    def post(self,request):
        url = request.POST.get('current_url')
        next_url = None
        if url and  '=' in url:
            next_url = url.split('=')[1]
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request,username=username,password=password)
        if user:
            # 登录成功，通过auth的login方法将用户写到session中
            auth.login(request,user)
            # 提交表单登录成功后跳转到用户自己的博客首页
            if not next_url:
                next_url = '/{}'.format(user.username)

            return JsonResponse({'state': True, 'Text': '登录成功！<a href={}>点击进入</a>'.format(next_url)})

        else:
            return JsonResponse({'state': False, 'Error': '登录失败！用户名或密码错误'})


# 退出登录
class Logout(View):
    def get(self,request):
        auth.logout(request)
        return redirect('/')

#个人站点
class HomeSite(View):
    def get(self,request,bottom_url,**kwargs):
        # 从url中获取bottom_url参数，根据获取的bottom_url查找对应站点
        blog = models.Blog.objects.filter(bottom_url=bottom_url).first()
        if not blog:
            return render(request, 'error.html', {'error_info': '没有对应的个人博客！'})
        # 然后根据站点查找对应的用户名
        user = models.UserInfo.objects.filter(blog=blog).first()

        # 置顶的博客
        sticky_article_list = None
        # 要展示的博客
        article_list = None
        # 分页查看时网页后缀
        page_url = None
        # 根据**kwargs的值来判断用户进的是哪个页面（分类、时间归档、或者搜索），然后查询相对于的博客列表传递过去
        if not kwargs:
        # 如果kwargs没有接收值，那么说明是进入站点首页
            article_list = models.Article.objects.filter(user=user,is_post=True).order_by('-pk')
            sticky_article_list = article_list.filter(is_stick=1,is_post=True)
            page_url = bottom_url
        else:
            view = kwargs.get('view')
            condition = kwargs.get('condition')

            if view == 'category':
                article_list = models.Article.objects.filter(user=user,category__title=condition,is_post=True)
            elif view == 'search':
                article_list = models.Article.objects.filter(Q(title__contains=condition)|Q(articledetail__content__contains=condition)).filter(is_post=True)

            elif view == 'archive':
                year,month = condition.split('-')
                article_list = models.Article.objects.filter(is_post=True,user=user,create_time__year=year,create_time__month=month)

            page_url = '/{}/articles/{}/{}'.format(bottom_url, view, condition)

        # 分页展示
        page = request.GET.get('page',1)
        page_obj = Pagination(article_list.count(),page,page_url)
        if article_list:
            article_list = article_list[page_obj.start:page_obj.end]
        page_html = page_obj.page_html()
        data = {
            'blog':blog,
            'user':user,
            'bottom_url':bottom_url,
            'article_list':article_list,
            'sticky_article_list':sticky_article_list,
            'page_html':page_html,
        }
        return render(request,'home.html',data)

# 博客密码验证
class ArticlePwdValid(View):
    def post(self,request):
        article_id = request.POST.get('article_id')
        user_input_pwd = request.POST.get('pwd')

        article = models.Article.objects.filter(nid=article_id).first()
        if article.password == user_input_pwd:
            return JsonResponse({'state':1})
        else:
            return JsonResponse({'state':0})


# 博客详情
class ArticleDetail(View):
    def get(self,request,bottom_url,article_id):
        # 从url中获取bottom_url参数，根据获取的bottom_url查找对应站点
        blog = models.Blog.objects.filter(bottom_url=bottom_url).first()
        if not blog:
            return render(request, 'error.html', {'error_info': '没有找到对应的个人博客！'})
        # 然后根据站点查找对应的用户
        user = models.UserInfo.objects.filter(blog=blog).first()
        # 根据博客id查找当前篇博客
        article = models.Article.objects.filter(nid=article_id).first()
        if not article:
            return render(request, 'error.html', {'error_info': '没有找到对应的博客！'})
        # 根据博客查找博客的作者
        user2 = article.user
        # 判断根据后缀找的用户与根据博客id找的用户是否一致
        if user != user2:
        #   不一致，说明是非法的url输入
            return render(request, 'error.html', {'error_info': '没有找到对应的博客！'})

        comment_list = models.Comment.objects.filter(article=article,parent_comment_id=None)
        data = {
            'blog': blog,
            'user': user,
            'article': article,
            'bottom_url': bottom_url,
            'comment_list': comment_list,
        }
        return render(request,'article.html',data)

# 博客点赞与踩灭
class ArticlePoll(View):
    def post(self,request):
        user_id = request.user.pk
        if not user_id:
            return JsonResponse({'state': 0})

        article_id = request.POST.get('article_id')

        article = models.Article.objects.filter(nid=article_id).first()
        # 根据博客作者来判断是不是登录者本人在点赞
        if article.user == request.user:
            return JsonResponse({'state':8})

        is_up = request.POST.get('is_up')
        is_up = eval(is_up)
        try:
            with transaction.atomic():
                models.ArticleUpDown.objects.create(user_id=user_id,article_id=article_id,is_up=is_up)
                # 给博客的点赞数或者踩灭数字段+1
                if is_up:
                    article.up_count += 1
                else:
                    article.down_count += 1
                article.save()
            return JsonResponse({'state':1})
        except Exception as e:
            # 如果报错，说明用户之前已经对该篇文章点过赞或者踩过灭
            # 那么就获取用户点赞或者踩灭数据，以供前端展示
            is_up = models.ArticleUpDown.objects.filter(user_id=user_id,article_id=article_id).first().is_up
            return JsonResponse({'state':2,'is_up':is_up})

# 博客评论
class CommentPost(View):
    def post(self,request,**kwargs):

        if not kwargs:
            pid = None
        else:
            pid = kwargs['pid']

        article_id = request.POST.get('article_id')
        content = request.POST.get('comment_content')
        user = request.user

        try:
            with transaction.atomic():
                models.Comment.objects.create(
                    article_id = article_id,
                    user_id = user.nid,
                    content = content,
                    parent_comment_id = pid,
                )
                models.Article.objects.filter(nid=article_id).update(comment_count=F('comment_count')+1)
                return JsonResponse({'state':True})
        except Exception as e:
            return JsonResponse({'state':False})

#
# class I(View):
#     def get(self,request):
#         return render(request, 'manage/article-manage.html', locals())

# 后台管理视图导航
# manage/(article|category|friendlylink|user)
class Manage(View):
    @method_decorator(login_required)
    def get(self,request,view):
        user = request.user
        blog = user.blog
        bottom_url = blog.bottom_url
        # 分页展示的页面url
        page_url = 'manage/{}'.format(view)

        page = request.GET.get('page', 1)
        page_obj = None
        data_list = None
        # 数据
        try:
            # 如果数据库暂时没有数据，切片会报错
            if view == 'article':
                article_list = models.Article.objects.filter(user=user,is_post=True).order_by('-pk')
                page_obj = Pagination(article_list.count(), page, page_url)
                data_list = article_list[page_obj.start:page_obj.end]
            elif view == 'drafts':
                drafts_list = models.Article.objects.filter(user=user,is_post=False).order_by('-pk')
                page_obj = Pagination(drafts_list.count(), page, page_url)
                data_list = drafts_list[page_obj.start:page_obj.end]
            elif view == 'category':
                category_list = models.Category.objects.filter(blog=blog)
                page_obj = Pagination(category_list.count(), page, page_url,12)
                data_list = category_list[page_obj.start:page_obj.end]
            else:
                link_list = models.FriendlyLink.objects.filter(blog=blog)
                page_obj = Pagination(link_list.count(), page, page_url)
                data_list = link_list[page_obj.start:page_obj.end]
        except AssertionError:
            data_list = []
        # 分页
        page_html = page_obj.page_html()

        data = {
            'user':user,
            'blog':blog,
            'bottom_url':bottom_url,
            'page_html':page_html,
            'data_list':data_list,
        }
        return render(request,'manage/{}-manage.html'.format(view),data)

# 博客管理
class ArticleManage(View):
    def get(self,request,handle,**kwargs):
        if handle == 'add':
            category_list = models.Category.objects.filter(blog=request.user.blog)
            return render(request,'manage/article-post.html',{'category_list':category_list})
        if handle == 'drafts':
            category_list = models.Category.objects.filter(blog=request.user.blog)
            return render(request, 'manage/drafts-manage.html', {'category_list': category_list})

        if kwargs:
            article_id = kwargs.get('article_id')
            article = models.Article.objects.filter(nid=article_id).first()
            data = {'state': False}
            if not article:
                return render(request, 'error.html', {'error_info': '没有找到您要的博客'})
            if handle == 'delete':
                try:
                    article.delete()
                    data['state'] = True
                    return JsonResponse(data)
                except:return JsonResponse(data)
            if handle == 'stick':
                if article.is_stick == True:
                    data['state'] = 1
                    return JsonResponse(data)
                try:
                    article.is_stick = True
                    article.save()
                    data['state'] = True
                    return JsonResponse(data)
                except:
                    return JsonResponse(data)
            if handle == 'update':
                category_list = models.Category.objects.filter(blog=request.user.blog)
                # print(category_list)
                return render(request, 'manage/article-update.html', {'category_list': category_list,'article':article})
        return render(request, 'error.html', {'error_info': '非法输入！'})

    def post(self,request,handle,article_id):
        if handle == 'password':
            # 修改博客密码
            password = request.POST.get('pwd', None)
            print(article_id,password)
            models.Article.objects.filter(nid=article_id).update(password=password)
            return JsonResponse({'state': True})
            # try:
            #     models.Article.objects.filter(nid=article_id).update(password=password)
            #     return JsonResponse({'state': True})
            # except:
            #     return JsonResponse({'state': False})
        if handle in ['add','drafts','update']:
            # 判断是添加/编辑新博客到草稿箱还是直接发布
            if handle == 'drafts':
                is_post = False
            else:
                is_post = True

            user = request.user
            article_title = request.POST.get('blog_title')
            article_content = request.POST.get('blog_content')
            article_category = request.POST.getlist('category')
            article_password = request.POST.get('password')

            # 正则匹配过滤标签
            article_desc = re.compile(r'<[^>]+>',re.S).sub('',article_content)[:120]

            # beatifulsoup模块过滤标签
            # soup = BeautifulSoup(article_content,'html.parser')
            #
            # [s.extract() for s in soup('script')]
            # print(type(soup))
            # article_desc = soup.text
            # article_content = soup
            #
            # print(article_desc)

            is_stick = request.POST.get('zhiding')
            is_stick = True if is_stick == '1' else False

            data = {
                "user":user,
                'title': article_title,
                'password': article_password,
                'is_stick': is_stick,
                'is_post':is_post,
                'desc':article_desc
            }
            # 判断是否有article_id参数，如果有，说明是编辑，如果没有说明是新添加
            if not article_id:
                # 说明为添加
                with transaction.atomic():
                    article_obj = models.Article.objects.create(**data)
                    article_obj.category.set(article_category)
                    article_obj.save()
                    models.ArticleDetail.objects.create(content=article_content,article=article_obj)
            else:
            #     说明为编辑
                article = models.Article.objects.filter(nid=article_id)
                article.update(**data)
                article_obj = article.first()
                article_obj.category.set(article_category)
                article_obj.save()
                models.ArticleDetail.objects.filter(article_id=article_id).update(content=article_content)

            # 根据是否立即发布来返回不同的页面
            if is_post:
                return redirect('/manage/article')
            else:
                return redirect('/manage/drafts')

# 发布草稿箱博客
class PostDraftsBlog(View):
    def get(self, request):
        article_id = request.GET.get('blog_id')

        article = models.Article.objects.filter(nid=article_id).first()
        if not article:
            return render(request,'error.html',{'error_info':'没有找到对应的博客!!!'})
        # try:
        article.is_post = True
        article.save()
        return JsonResponse({'state': True})
        # except:
        #     return JsonResponse({'state': False})


# 分类管理
class CategoryManage(View):
    def get(self,request,handle,**kwargs):
        if kwargs:
            category_id = kwargs.get('category_id')
            category = models.Category.objects.filter(nid=category_id).first()
            if not category:
                return render(request, 'error.html', {'error_info': '没有找到对应的分类'})
            if handle == 'delete':
                try:
                    category.delete()
                    return JsonResponse({'state':True})
                except:
                    return JsonResponse({'state':False})
        return render(request, 'error.html', {'error_info': '非法输入！'})

    def post(self,request,handle,**kwargs):
        if kwargs:
            cate_id = kwargs.get('category_id')
        else:
            return render(request, 'error.html', {'error_info': '没有找到对应的分类'})

        cate_tilte = request.POST.get('cate_name')
        cate_desc = request.POST.get('cate_info')
        blog = request.user.blog
        if handle == 'update':
            # 修改分类
            models.Category.objects.filter(nid=cate_id).update(title=cate_tilte,desc=cate_desc)
            return JsonResponse({'state':True})

        if handle == 'add':
            try:
                models.Category.objects.create(title=cate_tilte,desc=cate_desc,blog=blog)
                # 获取新插入的分类的id  传递给页面  以供ajax使用
                cate_obj = models.Category.objects.order_by('nid').last()
                cate_id = cate_obj.pk
                return JsonResponse({'state':True, 'cate_id': cate_id})
            except:
                return JsonResponse({'state':False})

# 友情链接管理
class FriendlylinkManage(View):
    def get(self, request, handle, **kwargs):
        if kwargs:
            link_id = kwargs.get('link_id')
            link = models.FriendlyLink.objects.filter(nid=link_id).first()
            if not link:
                return render(request, 'error.html', {'error_info': '没有找到对应的友情链接'})
            if handle == 'delete':
                try:
                    link.delete()
                    return JsonResponse({'state': True})
                except:
                    return JsonResponse({'state': False})

        return render(request, 'error.html', {'error_info': '非法输入！'})

    def post(self,request,handle,**kwargs):
        if kwargs and handle == 'update':
            link_id = kwargs.get('link_id')
            blog = request.user.blog
            title = request.POST.get('link_title')
            url = request.POST.get('link_url')
            models.FriendlyLink.objects.filter(nid=link_id).update(blog=blog,title=title,url=url)
            return JsonResponse({'state':True})
        if handle == 'add':
            blog = request.user.blog
            title = request.POST.get('link_title')
            url = request.POST.get('link_url')
            models.FriendlyLink.objects.create(blog=blog,title=title,url=url)
            # 获取新插入的链接的id  传递给页面  以供ajax使用
            link_obj = models.FriendlyLink.objects.order_by('nid').last()
            link_id = link_obj.pk
            return JsonResponse({'state': True,'link_id':link_id})

# 用户信息修改
class UserInfoUpdate(View):
    def post(self,request,view):
        if view == 'avatar':
            avatar = request.FILES.get('avatar')
            user = request.user
            old_avatar = user.avatar
            old_avatar_path = 'blog/media' + '/' + str(old_avatar)
            try:
                user.avatar = avatar
                user.save()
                # 删除用户原来的头像
                if old_avatar_path.split('/')[-1] != 'default.png':
                    os.remove(old_avatar_path)
                data = {'state': 1}
            except:
                data = {'state': 0}

            return JsonResponse(data)

        elif view == 'wechat':
            wechat = request.FILES.get('wechat')
            user = request.user
            old_wechat = user.wechat
            old_wechat_path = 'blog/media' + '/' + str(old_wechat)
            try:
                user.wechat = wechat
                user.save()
                # 删除用户原来的头像
                if old_wechat_path.split('/')[-1] != 'default.jpg':
                    os.remove(old_wechat_path)
                data = {'state': 1}
            except:
                data = {'state': 0}

            return JsonResponse(data)

        elif view == 'password':
            old_pwd = request.POST.get('old_pwd')
            new_pwd1 = request.POST.get('new_pwd1')
            new_pwd2 = request.POST.get('new_pwd2')
            data = {'state': False, 'msg': ''}
            user = request.user

            if not auth.authenticate(request, username=user.username, password=old_pwd):
                data['msg'] = '旧密码不正确，请检查后重试！'
            elif new_pwd1 != new_pwd2:
                data['msg'] = '新密码两次输入不一致，请重新输入！'
            else:
                password_valid = MyValid.valid(new_pwd2, str_name='密码', is_loginname=True, max_length=16, less_length=8)
                if password_valid['state'] == False:
                    data['msg'] = '且'.join(password_valid['error_msg'])
                else:
                    try:
                        # ############此处为明文密码##################
                        user.password = new_pwd2
                        user.save()
                        data['state'] = True
                    except:
                        data['msg'] = '修改失败，请重试！'
            return JsonResponse(data)

        elif view == 'info_detail':
            nickname = request.POST.get('nickname')
            telephone = request.POST.get('telephone')
            email = request.POST.get('email')
            qq = request.POST.get('qq')
            site = request.POST.get('site')
            site_title = request.POST.get('site_title')
            signature = request.POST.get('signature')

            data = {'state': False, 'msg': ''}
            user = request.user

            nickname_valid = MyValid.valid(nickname, str_name='昵称', is_alnum=True, max_length=18, less_length=4)
            telephone_valid = MyValid.valid(telephone, str_name='电话', is_telephone=True)
            email_valid = MyValid.valid(email, str_name='邮箱', is_email=True)
            qq_valid = MyValid.valid(qq, str_name='QQ', is_digit=True, max_length=12, less_length=5)

            if nickname.strip() == '':
                data['msg'] = '昵称不能为空，请填写您的昵称'
                return JsonResponse(data)
            elif nickname_valid['state'] == False:
                data['msg'] = '且'.join(nickname_valid['error_msg'])
                return JsonResponse(data)
            # 可以为空的字段
            for field in ['telephone', 'email', 'qq']:
                if eval(field) != '':
                    if eval('%s_valid' % field)['state'] == False:
                        data['msg'] = '且'.join(eval('%s_valid' % field)['error_msg'])
                        return JsonResponse(data)

            if site.strip() == '':
                # 如果site为空，给一个默认值
                site = user.username
            else:
                site_valid = MyValid.valid(site, str_name='站点后缀', is_loginname=True, max_length=20, less_length=4)
                if site_valid['state'] == False:
                    data['msg'] = '且'.join(site_valid['error_msg'])
                    return JsonResponse(data)

            # 查看数据库有是否已经存在
            blog = models.Blog.objects.filter(bottom_url=site).first()
            if blog and blog.nid != user.blog.nid:
                data['msg'] = '该站点后缀已经被注册，换一个试试吧！'
                return JsonResponse(data)

            try:
                user.nick_name = nickname
                user.telephone = telephone
                user.email = email
                user.qq = qq
                user.signature = signature
                user.blog.bottom_url = site
                user.blog.title = site_title

                user.blog.save()
                user.save()

                data['state'] = True
            except:
                data['msg'] = '修改失败，请重试！'
            return JsonResponse(data)

        else:
            return render(request,'error.html',{'error_info':'操作有误，请重试'})
