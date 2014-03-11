from ...api import v1_api
from .resources import (
    ArticleResource,
    TagResource,
    UserResource)


v1_api.register(ArticleResource())
v1_api.register(TagResource())
v1_api.register(UserResource())
