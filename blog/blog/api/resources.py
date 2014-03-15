from django.contrib.auth import get_user_model
from django.conf.urls import url
from django.db.models import Q
from extendedmodelresource import ExtendedModelResource
from tastypie.authentication import (
    ApiKeyAuthentication,
    Authentication,
    MultiAuthentication)
from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
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

    def obj_get(self, bundle, **kwargs):
        if kwargs.get(self._meta.detail_uri_name) == 'me':
            # We would simply override the query -- since we already hit the
            # database once anyway
            bundle.obj = bundle.request.user
            return bundle.request.user
        else:
            return super(UserResource, self).obj_get(bundle, **kwargs)


# Tag resource for taggit model
class TagResource(ModelResource):
    count = fields.IntegerField(readonly=True)

    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'
        detail_uri_name = 'slug'
        allowed_methods = ['get']

    def dehydrate_count(self, bundle):
        return bundle.obj.taggit_taggeditem_items.count()


class ArticleResource(ExtendedModelResource):
    class AuthorResource(ModelResource):
        class Meta:
            queryset = get_user_model().objects.all()
            fields = ['id', 'first_name', 'last_name']
            include_resource_uri = False

    author = fields.ForeignKey(AuthorResource, 'author', full=True)
    tags = fields.ListField()

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
            'tags': ALL_WITH_RELATIONS,
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

        if not request.user.is_superuser:
            if request.user.is_anonymous():
                # Anonymous users should only get access to public posts only
                return object_list.exclude(is_private=True)
            else:
                # Actual users will get access to all their posts, but private
                # articles from other users are out of bounds
                return object_list.exclude(
                    ~Q(author=request.user), is_private=True)
        else:
            return object_list

    def obj_create(self, bundle, **kwargs):
        # Due to the fact that Taggit requires the Article to be created first
        # before tags has to be attached, we'd have to add the code to create
        # the tags here as well
        updated_bundle = super(ArticleResource, self).obj_create(
            bundle, **kwargs)

        tags = bundle.data.get('tags')
        if tags is not None:
            updated_bundle.obj.tags.add(*tags)

        return updated_bundle

    def hydrate_tags(self, bundle):
        tags = bundle.data.get('tags')
        if tags is not None and bundle.obj.id is not None:
            bundle.obj.tags.add(*tags)

        return bundle

    def dehydrate_tags(self, bundle):
        return list(bundle.obj.tags.slugs())

    def hydrate_author(self, bundle):
        # Auto-assign the author to the requesting user if it is not supplied
        if bundle.data.get('author') is None:
            bundle.obj.author = bundle.request.user

        return bundle
