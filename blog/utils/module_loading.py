import copy
from importlib import import_module
from django.conf import settings
from django.utils.module_loading import module_has_submodule


# Adapted from Django 1.7 -- deprecate when Django 1.7 is available
def autodiscover_modules(*args, **kwargs):
    """
    Auto-discover INSTALLED_APPS modules and fail silently when
    not present. This forces an import on them to register any admin bits they
    may want.

    You may provide a register_to keyword parameter as a way to access a
    registry. This register_to object must have a _registry instance variable
    to access it.
    """
    register_to = kwargs.get('register_to')
    for app in settings.INSTALLED_APPS:
        mod = import_module(app)

        # Attempt to import the app's module.
        try:
            if register_to:
                before_import_registry = copy.copy(register_to._registry)

            for module_to_search in args:
                import_module('{0}.{1}'.format(app, module_to_search))
        except:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            # (see #8245).
            if register_to:
                register_to._registry = before_import_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have an admin module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, module_to_search):
                raise
