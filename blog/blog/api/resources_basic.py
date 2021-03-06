from django.contrib.auth import get_user_model
from taggit.models import Tag
from tastypie.resources import ModelResource
from ..models import Article


# The user resource from Django Auth
class UserResource(ModelResource):
    class Meta:
        queryset = get_user_model().objects.all()
        resource_name = 'user'


# Tag resource for taggit model
class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'


class ArticleResource(ModelResource):
    class Meta:
        queryset = Article.objects.all()
        resource_name = 'article'
