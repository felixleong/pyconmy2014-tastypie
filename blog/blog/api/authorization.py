from django.core.exceptions import ObjectDoesNotExist
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


# NOTE: Consider this as your first line of defence :) -- you still have to
#       make sure
class ArticleAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list

    def read_detail(self, object_list, bundle):
        # Nor we we restrict reading of articles
        return True

    def create_list(self, object_list, bundle):
        if bundle.request.user.is_anonymous():
            raise Unauthorized('The request requires an authenticated user')

        # We assume that the author will be correctly assigned
        return object_list

    def create_detail(self, object_list, bundle):
        user = bundle.request.user
        if user.is_anonymous():
            raise Unauthorized('The request requires an authenticated user')

        return bundle.obj.author == user or user.is_superuser

    # NOTE: The approach to put_list (update list) in Tastypie is by deleting
    #       the existing resource and then recreate them
    def update_list(self, object_list, bundle):
        user = bundle.request.user
        if user.is_anonymous():
            raise Unauthorized('The request requires an authenticated user')

        for obj in object_list:
            if obj.author != user and not user.is_superuser:
                raise Unauthorized(
                    'User does not have the permission to update an article '
                    'they are not an author')

        return object_list

    def update_detail(self, object_list, bundle):
        user = bundle.request.user
        if user.is_anonymous():
            raise Unauthorized('The request requires an authenticated user')

        try:
            article = object_list.get(pk=bundle.obj.id)
            return (
                (article.author == user and bundle.obj.author == user) or
                user.is_superuser)
        except ObjectDoesNotExist:
            return False

    def delete_list(self, object_list, bundle):
        user = bundle.request.user
        if user.is_anonymous():
            raise Unauthorized('The request requires an authenticated user')

        allowed = []

        for obj in object_list:
            if obj.author == user or user.is_superuser:
                allowed.append(obj)

        return allowed

    def delete_detail(self, object_list, bundle):
        user = bundle.request.user
        if user.is_anonymous():
            raise Unauthorized('The request requires an authenticated user')

        return bundle.obj.author == user or user.is_superuser
