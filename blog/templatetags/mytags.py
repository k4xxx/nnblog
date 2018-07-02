from django.db.models import Count
# from django.shortcuts import Ren
from blog import models
from django import template
register=template.Library()

@register.inclusion_tag('sidebar.html')
def getSideBar(bottom_url):
    # 从url中获取bottom_url参数，根据获取的bottom_url查找对应站点
    blog = models.Blog.objects.filter(bottom_url=bottom_url).first()
    # if not blog:
    #     return render(request, 'error.html', {'error_info': '没有对应的个人博客！'})
    # 然后根据站点查找对应的用户名
    user = models.UserInfo.objects.filter(blog=blog).first()
    # 然后在根据用户查找所对应的博客、分类等数据，展示到该用户的主页上
    link_list = models.FriendlyLink.objects.filter(blog=blog)
    category_title_and_count = models.Category.objects.filter(blog=blog).annotate(count=Count('article')).values(
        'title', 'count')

    # # 按照日期的年月来分组
    article_time_and_count = models.Article.objects.filter(user=user).extra(
        select={"time_ym": "DATE_FORMAT(create_time,'%%Y-%%m')"}).values(
        "time_ym").annotate(c=Count("nid")).values("time_ym", "c")

    data = {
        'user':user,
        'link_list': link_list,
        'bottom_url':bottom_url,
        'category_title_and_count': category_title_and_count,
        'article_time_and_count': article_time_and_count,
    }
    return data