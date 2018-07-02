import os
import django
import random
from MyBlog import models

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    django.setup()

    # 批量插入100条博客
    blog_list = []
    for i in range(100):
        blog_obj = models.Blog(
            title='博客标题{}'.format(i),
            content='博客内容{}'.format(i),
            category=random.choice(2,3),
       )

    models.Blog.objects.bulk_create(blog_list)