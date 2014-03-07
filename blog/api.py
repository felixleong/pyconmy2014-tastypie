from tastypie.api import Api
from blog.utils.module_loading import autodiscover_modules
#from django.utils.module_loading import autodiscover_modules


v1_api = Api(api_name='v1')


def autodiscover():
    autodiscover_modules('api')
