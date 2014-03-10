from django.contrib.auth import get_user_model
from tastypie.resources import ModelResource
from taggit.models import Tag
from .models import Article
from ..api import v1_api


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


v1_api.register(UserResource())
v1_api.register(TagResource())
v1_api.register(ArticleResource())
