from django.contrib.auth import get_user_model
from django.conf.urls import url
from django.db.models import Q
from extendedmodelresource import ExtendedModelResource
from tastypie.authentication import (
    ApiKeyAuthentication,
    Authentication,
    MultiAuthentication)
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.resources import ModelResource, ALL
from tastypie.utils import trailing_slash
from taggit.models import Tag
from .authorization import ArticleAuthorization
from ..models import Article


# The user resource from Django Auth
class UserResource(ExtendedModelResource):
    class Meta:
        queryset = get_user_model().objects.all()
        resource_name = 'user'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'put']
        excludes = ['password', 'is_staff', 'is_superuser', 'last_login']
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()

    class Nested:
        article = fields.ToManyField(
            'blog.blog.api.ArticleResource', 'article_set')
        # NOTE: If DB optimization is important, you can use the following
        #       statement instead
        #article = fields.ToManyField(
            #'blog.blog.api.ArticleResource',
            #lambda obj: obj.article_set.prefetch_related('tags', 'author'))

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>{0})/(?P<{1}>me){2}$".format(
                self._meta.resource_name, self._meta.detail_uri_name,
                trailing_slash()),
                self.wrap_view('dispatch_detail'),
                name='api_dispatch_detail'),
            url(
                r"^(?P<resource_name>{0})/(?P<{1}>me)/(?P<nested_name>article)"
                r"{2}$".format(
                    self._meta.resource_name, self._meta.detail_uri_name,
                    trailing_slash()),
                self.wrap_view('dispatch_nested'),
                name='api_dispatch_nested'),
        ]

    def dispatch_nested(self, request, **kwargs):
        self.is_authenticated(request)
        if kwargs.get(self._meta.detail_uri_name) == 'me':
            kwargs[self._meta.detail_uri_name] = request.user.id

        return super(UserResource, self).dispatch_nested(request, **kwargs)

    def get_detail(self, request, **kwargs):
        if kwargs.get(self._meta.detail_uri_name) == 'me':
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


class ArticleResource(ExtendedModelResource):
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
            'title': ALL,
            'date_published': ['gt', 'gte', 'lt', 'lte']
        }

    def prepend_urls(self):
        # With this setup, Article.slug fields should never be a number
        # But for the sample project, this restriction is not implemented yet
        return [
            url(r"^(?P<resource_name>{0})/(?P<pk>\d+){1}$".format(
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_detail'),
                name='api_dispatch_detail'),
        ]

    def get_object_list(self, request):
        object_list = super(ArticleResource, self).get_object_list(request)

        if request.user is None:
            return object_list.exclude(
                ~Q(author=request.user), is_private=True)
        elif not request.user.is_superuser():
            return object_list.exclude(is_private=True)
        else:
            return object_list
