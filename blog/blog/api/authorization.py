from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from django.db.models import Q


# NOTE: Consider this as your first line of defence :) -- you still have to
#       make sure
class ArticleAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        # No restrictions to the listing
        if bundle.request.user is None:
            return object_list.exclude(
                ~Q(author=bundle.request.user), is_private=True)
        else:
            return object_list.exclude(is_private=True)

    def read_detail(self, object_list, bundle):
        # Nor we we restrict reading of articles
        return True

    def create_list(self, object_list, bundle):
        # We would be assigning it on our own
        if bundle.request.user is None:
            return Unauthorized('The request requires an authenticated user')

        return object_list

    def create_detail(self, object_list, bundle):
        if bundle.request.user is None:
            return Unauthorized('The request requires an authenticated user')

        return bundle.obj.author == bundle.request.user

    # NOTE: On "update_*" and "delete_*", the authorization check happens AFTER
    #       the object has been populated w/ the changes, so you probably want
    #       to do a pre-check.
    def update_list(self, object_list, bundle):
        allowed = []

        for obj in object_list:
            if obj.author == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.author == bundle.request.user

    def delete_list(self, object_list, bundle):
        allowed = []

        for obj in object_list:
            if obj.author == bundle.request.user:
                allowed.append(obj)

        return allowed

    def delete_detail(self, object_list, bundle):
        return bundle.obj.author == bundle.request.user
