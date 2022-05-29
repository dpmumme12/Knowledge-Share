import uuid as uuid_lib
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags
from django.utils.text import Truncator
from KnowledgeShare.utils.models import TimeStampedModel

# Create your models here.
class Article(TimeStampedModel):

    class Article_Status(models.IntegerChoices):
        DRAFT = 1, _('Draft')
        PUBLISHED = 2, _('Published')
        ARCHIVED = 3, _('Archived')

    class Version_Status(models.IntegerChoices):
        ACTIVE = 4, _('Active')
        HISTORY = 5, _('History')
        NEW_VERSION = 6, _('New Version')

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=200, blank=True)
    article_status_id = models.SmallIntegerField(choices=Article_Status.choices)
    content = models.TextField(blank=True)
    version = models.IntegerField(default=0)
    version_status_id = models.SmallIntegerField(choices=Version_Status.choices)
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE, null=True, blank=True)
    foreign_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                           through='Article_User',
                                           through_fields=('article', 'user'),
                                           related_name='foreign_articles')

    @property
    def truncated_content(self):
        content = strip_tags(self.content)
        return Truncator(content).words(20)


class ArticleImage(models.Model):
    article_id = models.ForeignKey('Article', on_delete=models.CASCADE)
    image = models.ImageField()


class Article_User(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['article', 'user'], name='unique article_user')
        ]


class Folder(TimeStampedModel):
    name = models.CharField(max_length=200)
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def UserFolders(user):
        """
        Returns a list of the users folders
        """
        return list(Folder.objects.filter(owner=user))