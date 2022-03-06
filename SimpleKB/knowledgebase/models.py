from distutils.command.upload import upload
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from SimpleKB.utils.models import TimeStampedModel

# Create your models here.
class Article(TimeStampedModel):

    class Status(models.IntegerChoices):
        DRAFT = 1, _('Draft')
        ACTIVE = 2, _('Active')
        HISTORY = 3, _('History')
        ARCHIVED = 4, _('Archived')

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=200, blank=True)
    article_status = models.SmallIntegerField(choices=Status.choices)
    content = models.TextField(blank=True)
    version = models.IntegerField(default=0)


class ArticleImage(models.Model):
    article_id = models.ForeignKey('Article', on_delete=models.CASCADE)
    image = models.ImageField()
