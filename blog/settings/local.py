from blog.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n-f+(oo7to!p1q^cf&y48+wf*&(z@tkh9(n-)d0#3+g@)ngtm*)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
