from django.contrib.auth.models import User
from .models import Article, ArticleType
import time

# for test
def test_add_article(l, r): 
    super_user = User.objects.all()[0]
    for i in range(l,r+1):
        article = Article()
        article.title = "test {}".format(i)
        article.content = "xxxxx {}".format(i)
        article.article_type = ArticleType.objects.all()[i%2]
        article.author = super_user
        article.save()
        time.sleep(0.0001)