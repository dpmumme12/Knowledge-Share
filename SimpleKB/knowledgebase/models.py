import uuid as uuid_lib
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from SimpleKB.utils.models import TimeStampedModel

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


class ArticleImage(models.Model):
    article_id = models.ForeignKey('Article', on_delete=models.CASCADE)
    image = models.ImageField()


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
