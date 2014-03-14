from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import (
    CreationDateTimeField,
    ModificationDateTimeField)
from taggit.managers import TaggableManager


class Article(models.Model):
    title = models.CharField(_('title'), max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True)
    body = models.TextField(_('body text'))
    is_private = models.BooleanField(_('Make private'), default=False)
    time_created = CreationDateTimeField(_('time created'))
    time_published = models.DateTimeField(
        _('time published'), default=timezone.now())
    time_modified = ModificationDateTimeField(_('time modified'))
    tags = TaggableManager()
    slug = models.SlugField(_('slug'))
    summary = models.TextField(
        _('summary'), default=None, blank=True, null=True)
