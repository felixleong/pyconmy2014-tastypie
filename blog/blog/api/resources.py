from django.contrib.auth import get_user_model
from django.conf.urls import url
#from extendedmodelresource import ExtendedModelResource
from tastypie.authentication import (
    ApiKeyAuthentication,
    Authentication,
    MultiAuthentication)
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from taggit.models import Tag
from ..models import Article


# The user resource from Django Auth
class UserResource(ModelResource):
    class Meta:
        queryset = get_user_model().objects.all()
        resource_name = 'user'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'put']
        excludes = ['password', 'is_staff', 'is_superuser', 'last_login']
        authentication = ApiKeyAuthentication()


# Tag resource for taggit model
class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'
        detail_uri_name = 'slug'


class ArticleResource(ModelResource):
    class AuthorResource(ModelResource):
        class Meta:
            queryset = get_user_model().objects.all()
            fields = ['id', 'first_name', 'last_name']
            include_resource_uri = False

    author = fields.ForeignKey(AuthorResource, 'author', full=True)
    # If we prefer to have better API access to the tags, we should be doing
    # this
    # tags = fields.ToManyField(TagResource, 'tags')
    tags = fields.ToManyField(TagResource, 'tags')

    def dehydrate_tags(self, bundle):
        return list(bundle.obj.tags.slugs())

    class Meta:
        queryset = Article.objects.prefetch_related('tags', 'author').all()
        resource_name = 'article'
        authentication = MultiAuthentication(
            ApiKeyAuthentication(),
            Authentication())
        detail_uri_name = 'slug'

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>{0})/(?P<pk>\d+){1}$".format(
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_detail'),
                name='api_dispatch_detail'),
            url(r"^(?P<resource_name>{0})/search{1}$".format(
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_list_search'),
                name='api_get_list_search'),
        ]
