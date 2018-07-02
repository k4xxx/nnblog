# import win_unicode_console
# win_unicode_console.enable()
from django.db import models
#
# # Create your models here.

from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """
    用户信息
    """
    nid = models.AutoField(primary_key=True)
    nick_name = models.CharField(max_length=36,null=False)
    telephone = models.CharField(max_length=11, null=True)
    avatar = models.FileField(upload_to='avatars/', default="avatars/default.png")
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    qq = models.CharField(verbose_name='QQ',max_length=12)
    wechat = models.ImageField(upload_to='wechat/',verbose_name='微信二维码',default='wechat/default.jpg')
    signature = models.TextField(verbose_name='用户签名',max_length=120)

    blog = models.OneToOneField(to='Blog', to_field='nid', null=True)

    def __str__(self):
        return self.username


class Blog(models.Model):
    """
    博客站点信息
    """

    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    bottom_url = models.CharField(verbose_name='个人博客后缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)

    def __str__(self):
        return self.title


class Category(models.Model):
    """
    博主个人文章分类表
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    desc = models.CharField(verbose_name='分类描述', max_length=32,default=None)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')

    def __str__(self):
        return self.title


class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')

    def __str__(self):
        return self.title


class Article(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章描述')
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    password = models.CharField(verbose_name='博客密码',max_length=16)
    is_post = models.BooleanField(verbose_name='是否发布',default=True)
    is_stick = models.BooleanField(verbose_name='是否置顶',default=False)
    category = models.ManyToManyField(to='Category', null=True)
    user = models.ForeignKey(verbose_name='作者', to='UserInfo', to_field='nid')

    comment_count = models.IntegerField(verbose_name='评论数',default=0)
    up_count = models.IntegerField(verbose_name='点赞数',default=0)
    down_count = models.IntegerField(verbose_name='踩灭数',default=0)

    # content = models.OneToOneField(to='ArticleDetail', to_field='nid')

    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )

    def __str__(self):
        return self.title


class ArticleDetail(models.Model):
    """
    文章详细表
    """
    nid = models.AutoField(primary_key=True)
    content = models.TextField()
    article = models.OneToOneField(to='Article', to_field='nid')


class Article2Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid')
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid')

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]

    def __str__(self):
        v = self.article.title + "--" + self.tag.title
        return v


class ArticleUpDown(models.Model):
    """
    点赞表
    """

    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInfo', null=True)
    article = models.ForeignKey("Article", null=True)
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = [
            ('article', 'user'),
        ]


class Comment(models.Model):
    """

    评论表

    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid')
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid')
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    parent_comment = models.ForeignKey('self', null=True)

    def __str__(self):
        return self.content


class FriendlyLink(models.Model):
    '''友情链接表'''
    nid = models.AutoField(primary_key=True)
    title =models.CharField(max_length=32)
    url = models.CharField(max_length=64)
    describe = models.CharField(max_length=32, null=True)   #描述
    blog = models.ForeignKey(to='Blog')

