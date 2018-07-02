# from django.shortcuts import render
# from django.shortcuts import redirect
# from MyBlog import models
#
# class GetData:
#     '''
#     获取数据库的数据
#     '''
#     @staticmethod
#     def getBlog(request,blog_id=None,status=None,category_id=None,is_sticky=None):
#         '''
#         从数据库里获取置顶的博客列表
#         :param blog_id: 博客ID
#         :param status: 博客的发布状态（bool值，表示已发布或者在草稿箱）
#         :param category_id: 博客分类ID
#         :param is_sticky: 博客是否置顶
#         :return: 筛选过后的博客列表
#         '''
#         print(blog_id)
#         print(status)
#
#         if is_sticky:
#             # 说明要获取置顶博客
#             return models.Blog.objects.filter(is_sticky=True)
#         if category_id:
#             # 说明要根据分类获取博客列表
#             if category_id == '0':
#                 # 展示未分类博客
#                 blogs = models.Blog.objects.filter(category=None)
#             else:
#                 blogs = models.Blog.objects.filter(category=category_id)
#                 # 获取当前分类名称以供页面标题使用
#                 category_list = models.Category.objects.filter(id=category_id)
#                 if not category_list:
#                     return render(request, 'error.html', {'error_info': '抱歉，没有所选分类！'})
#                 else:
#                     category = category_list[0]
#                     # return blogs, category
#             return blogs
#
#
#         if not(blog_id or status):
#             # 如果没有传ID或者状态为None（没传）或者为False，会进入此判断
#             # 如果status为False
#             if str(status) == 'False':
#                 blog_list = models.Blog.objects.filter(is_post=False)
#                 return blog_list
#             # 否则说明id和status都没有传递过来，表示需要获取所有blog
#             blog_list = models.Blog.objects.all()
#             print('11111111111')
#             return blog_list
#         elif not blog_id and status:
#             # 如果ID为None并且状态有值且不为True，说明需要查看已发布的博客列表
#             # 判断传递来的status是否合法（是否为bool值）
#             # if str(status) not in ('True','False'):
#             if str(status) != 'True':
#                 return '非法链接'
#             blog_list = models.Blog.objects.filter(is_post=status)
#             print('22222222222222......',blog_list.count())
#             return blog_list
#         elif not status and blog_id:
#             print('没有状态有ID')
#             # 如果状态为None并且ID不为空
#             # 验证ID是否合法
#             if not blog_id.isdigit():
#                 print('id不为')
#                 return '博客ID只能为数字哦'
#             # 根据id获取博客对象
#             # 根据ID查找最多只能找到一篇博客，但是如果id在数据库不存在，那么用get方法会报错，所有只能用filter
#             blog = models.Blog.objects.filter(id=blog_id)
#             # 查看是否存在id为该id的博客
#             if not blog:
#                 # 说明根据ID没有查到对应的博客
#                 return '您要查找的博客不存在哦'
#             else:
#                 # 查到了，就获取列表里的元素（只有一个)
#                 blog = blog[0]
#                 if blog.is_post == False and request.COOKIES.get('username') == None:
#                     # 如果博客未发布并且非登录状态
#                     return '您要查找的博客还没发布哦，请登录后查看'
#                 # print('33333333')
#                 return blog
#
#     @staticmethod
#     def getCookiesUser(request):
#         username = request.COOKIES.get('username')
#         user = models.User.objects.filter(username=username)
#         if user:
#             user = user[0]
#         return user
#
#     @staticmethod
#     def getCategory(category_id=None):
#         if not category_id:
#             # 获取所有分类
#             return models.Category.objects.all()
#         else:
#             if not category_id.isdigit():
#                 return '抱歉，非法输入！'
#             else:
#                 category = models.Category.objects.filter(id=category_id)
#                 if category:
#                     category = category[0]
#                     return category
#                 else:
#                     return '抱歉，您删除的分类不存在！'
#
#     @staticmethod
#     def getFriendLink(link_id=None):
#         if not link_id:
#             # 获取所有友情链接
#             return models.FriendlyLink.objects.all()
#         else:
#             if not link_id.isdigit():
#                 return '抱歉，非法输入！'
#             else:
#                 link = models.FriendlyLink.objects.filter(id=link_id)
#                 if link:
#                     link = link[0]
#                     return link
#                 else:
#                     return '抱歉，您删除的友情链接ID不存在！'
#
#     @staticmethod
#     def getBlogCount(category_id=None):
#         '''
#         查询根据分类id查询属于该分类的博客个数
#         :param category_id: 分类ID
#         :return: int
#         '''
#         if not category_id:
#             # 返回未分类博客个数
#             count = models.Blog.objects.filter(category=None).count()
#         else:
#             count = models.Blog.objects.filter(category=category_id).count()
#         return count