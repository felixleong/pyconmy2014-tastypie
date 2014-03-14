.. Creating Powerful RESTful APIs with Django-Tastypie slides file, created by
   hieroglyph-quickstart on Fri Mar 14 15:11:09 2014.

Creating Powerful RESTful APIs with Django-Tastypie
===================================================

`Seh Hui Leong <http://twitter.com/felixleong/>`_ |br|
March 2014, Mini PyCon Malaysia 2014

.. figure:: /_static/4687542962_87bdc4f9f0_b.jpg
    :class: fill

    CC-BY-NC-SA https://flic.kr/p/89dTdf

.. ifnotslides::

    .. toctree::
        :maxdepth: 2

ACT 1: RESTful is AWESOME!
--------------------------

.. figure:: /_static/4960389917_1d0b48f117_b.jpg
    :class: fill

    CC http://www.flickr.com/photos/mccun934/4960389917/

REST-what?
__________

- REpresentational State Transfer
- **Paradigm/Infrastructure pattern to designing easy-to-understand APIs**
    - Both **machine- and programmer-readable** without convoluted protocols
- Usually called **RESTful** because no one seems to agree what a perfect REST
  service is

Making the Perfect Bread and Bacon
__________________________________

- Thinking in **resources**
- **Uniform Resource Identifier/Locator (URI/URL)**
- **HTTP**: The perfect **uniform interface**

HTTP: The Perfect Fit (I)
_________________________

You can represent CRUD actions using **HTTP verbs**

:**Create**: POST
:**Retrieve**: GET
:**Update**: UPDATE
:**Delete**: DELETE

HTTP: The Perfect Fit (II)
__________________________

You can get status of your requests using **HTTP status codes**

==== ================================
Code Meaning
==== ================================
200  OK
201  Created
204  No-Content (i.e. return void)
400  Bad Request
401  Unauthorized
403  Forbidden
404  Not Found
500  Internal Server Error (OMG BUG!)
==== ================================

HTTP: The Perfect Fit (III)
___________________________

You can use **HTTP headers** to specify operating parameters of a transaction.

============== ==========================
Request header Description
============== ==========================
Accept         Content we want to request
Authorization  Authentication credentials
============== ==========================

=============== =============================================
Response header Description
=============== =============================================
Status          Status of the transaction 
Location        The destination URI (important for redirects)
=============== =============================================

ACT 2: Hello World, Tastypie!
-----------------------------

.. figure:: /_static/3294261072_c635d74ce8_o.jpg
    :class: fill

    CC-BY-NC https://flic.kr/p/626X3G

One Model Only Blog App
_______________________

.. code:: python

    from django_extensions.db.fields import (
        CreationDateTimeField,
        ModificationDateTimeField)
    from taggit.managers import TaggableManager

    class Article(models.Model):
        title = models.CharField(max_length=100)
        author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True)
        body = models.TextField()
        is_private = models.BooleanField(default=False)
        time_created = CreationDateTimeField()
        time_published = models.DateTimeField(default=timezone.now())
        time_modified = ModificationDateTimeField()
        tags = TaggableManager()
        slug = models.SlugField()
        summary = models.TextField(default=None, blank=True, null=True)

API Endpoints
_____________

All with **CRUD** operations [POST/GET/PUT/DELETE]

- /api/v1/user/
- /api/v1/user/:id/
- /api/v1/tag/
- /api/v1/tag/:id/
- /api/v1/article/
- /api/v1/article/:id/

Magic with The Least Lines! #1
______________________________

blog/blog/api.py

.. code:: python

    from django.contrib.auth import get_user_model
    from tastypie.resources import ModelResource
    from taggit.models import Tag
    from .models import Article

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

Magic with The Least Lines! #2
______________________________

blog/blog/api.py *(continued)*

.. code:: python

    class ArticleResource(ModelResource):
        class Meta:
            queryset = Article.objects.all()
            resource_name = 'article'

Magic with The Least Lines! #3
______________________________

blog/urls.py

.. code:: python

    from tastypie.api import Api
    from blog.api import UserResource, TagResource, ArticleResource

    v1_api = Api(api_name='v1')
    v1_api.register(UserResource())
    v1_api.register(TagResource())
    v1_api.register(ArticleResource())

    urlpatterns = patterns(
        '',
        url(r'^api/', include(api.v1_api.urls)),
    )

ACT 3: Building Tastypie APIs for The Real World
------------------------------------------------

.. figure:: /_static/5650815548_59e3c82b6a_b.jpg
    :class: fill

    CC-BY-NC https://flic.kr/p/9BkUAh

Limit What Data To Show
_______________________

.. code:: python

    class UserResource(ModelResource):
        class Meta:
            excludes = ['password', 'is_staff', 'is_superuser', 'last_login']
            # ... or do this, if you prefer explicit white-listing instead
            #fields = ['id', 'first_name', 'last_name']

You Shall Not Pass! *(Authentication)*
______________________________________ 

.. code:: python

    from tastypie.authentication import (
        ApiKeyAuthentication,
        Authentication,
        MultiAuthentication)

    class UserResource(ExtendedModelResource):
        class Meta:
            authentication = ApiKeyAuthentication()

    class ArticleResource(ModelResource):
        class Meta:
            authentication = MultiAuthentication(
                ApiKeyAuthentication(), Authentication())

Supports HTTP-Basic, HTTP-Digest, API key, Session, OAuth 1, or
`roll out your own <https://django-tastypie.readthedocs.org/en/latest/authentication.html#implementing-your-own-authentication-authorization>`_.

Full CRUD Can Be Dangerous
__________________________

.. code:: python

    class UserResource(ModelResource):
        class Meta:
            # ... Would only allow the retrieval of user listing, and support
            # the update of user details
            list_allowed_methods = ['get']
            detail_allowed_methods = ['get', 'put']

Limit The Dataset To Operate On
_______________________________

.. code:: python

    from django.db.models import Q

    class ArticleResource(ModelResource):
        def get_object_list(self, request):
            object_list = super(ArticleResource, self).get_object_list(request)

            if not request.user.is_superuser:
                return object_list.exclude(is_private=True)
            else:
                return object_list

Laying Out Authorization Boundaries
___________________________________

.. code:: python

    from tastypie.authorization import DjangoAuthorization
    from .authorization import ArticleAuthorization

    class UserResource(ModelResource):
        class Meta:
            # Relies on Django permissions as authorization
            authorization = DjangoAuthorization()

    class ArticleResource(ExtendedModelResource):
        class Meta:
            # We need more fine grain control as we only allow original authors
            # to edit their own entries
            authorization = ArticleAuthorization()

**Refer to blog/blog/api/authorization.py** on a sample of how to implement a
custom authorization handler.

Adding Custom API Endpoints
___________________________

Adding a convenience endpoint /api/v1/users/me/

.. code:: python

    class UserResource(ModelResource):
        def prepend_urls(self):
            return [
                url(r"^(?P<resource_name>{0})/(?P<{1}>me){2}$".format(
                    self._meta.resource_name, self._meta.detail_uri_name,
                    trailing_slash()),
                    self.wrap_view('dispatch_detail'),
                    name='api_dispatch_detail'), ]

        def get_detail(self, request, **kwargs):
            if kwargs.get(self._meta.detail_uri_name) == 'me':
                kwargs[self._meta.detail_uri_name] = request.user.id

            return super(UserResource, self).get_detail(request, **kwargs)

        def put_detail(self, request, **kwargs):
            if kwargs[self._meta.detail_uri_name] == 'me':
                kwargs[self._meta.detail_uri_name] = request.user.id

            return super(UserResource, self).put_detail(request, **kwargs)

Change The Details Identifier Field
___________________________________

Like slugs instead of IDs? No problem!

.. code:: python

    class TagResource(ModelResource):
        class Meta:
            # THERE! So simple!
            detail_uri_name = 'slug'

Nested Foreign Keys and Related Querysets
_________________________________________

.. code:: python

    class ArticleResource(ExtendedModelResource):
        class AuthorResource(ModelResource):
            class Meta:
                queryset = get_user_model().objects.all()
                fields = ['id', 'first_name', 'last_name']
                include_resource_uri = False

        author = fields.ForeignKey(AuthorResource, 'author', full=True)
        # We can also reuse our User Resource instead for more data
        # author = fields.ForeignKey(UserResource, 'author', full=True)

        # Under normal circumstances, only the API resource URI is used
        tags = fields.ToManyField(TagResource, 'tags')

Adding Custom Fields
____________________

We can also add custom fields that is not defined in our models. For example,
useful aggregate fields.

.. code:: python

    class TagResource(ModelResource):
        count = fields.IntegerField(readonly=True)

        def dehydrate_count(self, bundle):
            return bundle.obj.taggit_taggeditem_items.count()

Add Filter Based Querying
_________________________

To support GET list filtering based on criteria on fields.

e.g. /api/v1/article/?title__icontains=malaysia

.. code:: python

    from tastypie.resources import ModelResource, ALL

    class ArticleResource(ModelResource):
        class Meta:
            filtering = {
                'title': ALL,
                'tags': ALL_WITH_RELATIONS,
                'date_published': ['gt', 'gte', 'lt', 'lte']
            }

Note that ALL (and ALL_WITH_RELATIONS) supports Django ORM query parameters.

How to Make Sure Incoming Data is Validated?
____________________________________________

.. code:: python

    from tastypie.validation import CleanedDataFormValidation
    from ..forms import ArticleForm

    class ArticleResource(ExtendedModelResource):
        class Meta:
            validation = CleanedDataFormValidation(form_class=ArticleForm)

Complex URL Representations
___________________________

- Example: How to query articles written by a user?
- **/api/v1/article/?author=1** vs. **/api/v1/user/1/article/**
- Use `django-tastypie-extendedmodelresource`_ 

.. code:: python

    from extendedmodelresource import ExtendedModelResource

    # Inherit from EMR instead...
    class UserResource(ExtendedModelResource):
        class Nested:
            article = fields.ToManyField(
                'blog.blog.api.ArticleResource', 'article_set')

    # Must also be EMR
    class ArticleResource(ExtendedModelResource):
        pass

.. _django-tastypie-extendedmodelresource: https://github.com/felixleong/django-tastypie-extendedmodelresource/

Performance Starts With Queryset Optimization
_____________________________________________

- Normal ORM optimization tips apply -- **`select_related()` and `prefetch_related`
  are your friends** :).
- Whatever you read about DB/ORM optimization, use it. Apply it to
  `Resource.Meta.queryset` or `Resource.get_object_list`.

.. code:: python

    class ArticleResource(ExtendedModelResource):
        class Meta:
            queryset = Article.objects.prefetch_related('tags', 'author').all()

Note on Caching on Tastypie
___________________________

- Tastypie only supports the following caching strategies:
    - **Queryset caching**: the cached queryset is only used for all the
      `\*_detail()` functions (i.e. only applies to queries that affect a
      specific resource)
    - Client side caching (i.e. setting the Cache-Control HTTP header)
- Tastypie doesn't handle caching of serialized output

Caching Serialized Output on Tastypie
_____________________________________

- Use a caching proxy like `Varnish`_
- Personally have implemented a `Automatic Generation-Based Action Caching`_
  approach using a class mixin that can be used by a `ModelResource` and
  hooked up `post_save` signals to update the generation count
    - *Not included in the sample source :(*

.. _Varnish: https://www.varnish-cache.org/
.. _Automatic Generation-Based Action Caching: http://cdn.oreillystatic.com/en/assets/1/event/27/Accelerate%20your%20Rails%20Site%20with%20Automatic%20Generation-based%20Action%20Caching%20Presentation%201.pdf

Tastypie `urlpattern` Auto-discovery
____________________________________

- Do it like `django.contrib.auth` -- declare once and forget
- Refer to **blog/api.py** and **blog/utils/module_loading.py**
- Django 1.7 will have `django.utils.module_loading.autodiscover_modules`

FINALE: You Are Now Smarter!
----------------------------

.. figure:: /_static/6966069023_5512204921_b.jpg
    :class: fill

    CC-BY http://www.flickr.com/photos/sylvainkalache/6966069023/

You Have Learned…
_________________

- What is **RESTful API**?
- It's **easy to get started** with Tastypie
- And how to **flesh it out** with real-world constraints:
    - Basic CRUD restrictions
    - Adding custom API endpoints
    - Authentication and authorization
    - Customizing data fields of resources
    - Quick optimization wins

GIMME EVERYTHING!
_________________

**Code, Demo, Presentation**

http://github.com/felixleong/pyconmy2014-tastypie/

:Email: felixleong@gmail.com
:Facebook: http://facebook.com/leongsh/
:Twitter: http://twitter.com/felixleong/

References
__________

- Tastypie
    - https://django-tastypie.readthedocs.org/en/latest/
- Tastypie-ExtendedModelResource
    - https://github.com/felixleong/django-tastypie-extendedmodelresource/
- My previous talk, RESTful API 101
    - https://github.com/felixleong/wckl_restapi_talk/
- REST in Practice, *by Jim, Savas and Ian* (O'Reilly)
    - http://shop.oreilly.com/product/9780596805838.do

License
_______

This work is licensed under a `Creative Commons Attribution-ShareAlike 3.0 Unported License`_.

.. _Creative Commons Attribution-ShareAlike 3.0 Unported License: http://creativecommons.org/licenses/by-sa/3.0/deed.en_US

.. CUSTOM DEFINITIONS

.. |br| raw:: html

    <br />
