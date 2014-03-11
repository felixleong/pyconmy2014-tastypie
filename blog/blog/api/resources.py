from django.contrib.auth import get_user_model
#from extendedmodelresource import ExtendedModelResource
from tastypie.authentication import (
    ApiKeyAuthentication,
    Authentication,
    MultiAuthentication)
from tastypie.resources import ModelResource
from taggit.models import Tag
from .models import Article


# The user resource from Django Auth
class UserResource(ModelResource):
    class Meta:
        queryset = get_user_model().objects.all()
        resource_name = 'user'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'put']
        authentication = ApiKeyAuthentication()


# Tag resource for taggit model
class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'


class ArticleResource(ModelResource):
    class Meta:
        queryset = Article.objects.all()
        resource_name = 'article'
        authentication = MultiAuthentication(
            ApiKeyAuthentication(),
            Authentication())
