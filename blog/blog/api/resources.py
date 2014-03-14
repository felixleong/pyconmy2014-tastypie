from django.contrib.auth import get_user_model
from django.conf.urls import url
#from extendedmodelresource import ExtendedModelResource
from tastypie.authentication import (
    ApiKeyAuthentication,
    Authentication,
    MultiAuthentication)
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from taggit.models import Tag
from .authorization import ArticleAuthorization
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
        authorization = DjangoAuthorization()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>{0})/me{1}$".format(
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_detail_me'),
                name='api_dispatch_detail_me'),
        ]

    def dispatch_detail_me(self, request, **kwargs):
        kwargs[self._meta.detail_uri_name] = 'me'
        return super(UserResource, self).dispatch_detail(request, **kwargs)

    def get_detail(self, request, **kwargs):
        if kwargs[self._meta.detail_uri_name] == 'me':
            kwargs[self._meta.detail_uri_name] = request.user.id

        return super(UserResource, self).get_detail(request, **kwargs)

    def put_detail(self, request, **kwargs):
        if kwargs[self._meta.detail_uri_name] == 'me':
            kwargs[self._meta.detail_uri_name] = request.user.id

        return super(UserResource, self).put_detail(request, **kwargs)


# Tag resource for taggit model
class TagResource(ModelResource):
    count = fields.IntegerField(readonly=True)

    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'
        detail_uri_name = 'slug'

    def dehydrate_count(self, bundle):
        return bundle.obj.taggit_taggeditem_items.count()


class ArticleResource(ModelResource):
    class AuthorResource(ModelResource):
        class Meta:
            queryset = get_user_model().objects.all()
            fields = ['id', 'first_name', 'last_name']
            include_resource_uri = False

    author = fields.ForeignKey(AuthorResource, 'author', full=True)
    tags = fields.ToManyField(TagResource, 'tags')

    #NOTE: If you prefer that it's just a list of tag slug, we can use a custom
    #      field instead
    #tags = fields.ToManyField(TagResource, 'tags')

    #def dehydrate_tags(self, bundle):
        #return list(bundle.obj.tags.slugs())

    class Meta:
        queryset = Article.objects.prefetch_related('tags', 'author').all()
        resource_name = 'article'
        authentication = MultiAuthentication(
            ApiKeyAuthentication(),
            Authentication())
        authorization = ArticleAuthorization()
        detail_uri_name = 'slug'
        filtering = {
            'date_published': ['gt', 'gte', 'lt', 'lte']
        }

    def prepend_urls(self):
        # With this setup, Article.slug fields should never be a number or
        # named "search". But for the sample project, this restriction is not
        # implemented yet
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
