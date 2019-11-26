from django.db import models
from uuslug import uuslug

from article.base.models import AbstractArticle
from article.constant import MAX_SLUG_LENGTH
from record.models import SimpleRecord, DetailedRecord
from reply.models import BaseReply


class ArticleRecord(SimpleRecord):
    pass


# The base class of all sub-class of article
class Article(AbstractArticle):
    record = models.OneToOneField(ArticleRecord, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ArticleVote(DetailedRecord):
    attitude = models.BooleanField(default=False)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)


# The home page article model
class HomeArticle(Article):
    slug = models.CharField(max_length=MAX_SLUG_LENGTH)
    excerpt = models.TextField(blank=True)
    rank = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super().save(*args, **kwargs)


# The user article model
class UserArticle(Article):
    pass


class ArticleComment(BaseReply):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
