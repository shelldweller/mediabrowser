import sys
import os.path

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = 'Mary had a little lamb. His fleece was white as snow.'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, "data", "db.sqlite3"),
    }
}

LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('bg', "Bulgarian"),
    ('cs', "Czech"),
    ('da', "Danish"),    
    ('de', "German"),
    ('es', "Spanish"),
    ('fi', "Finnish"),
    ('fr', "French"),
    ('hr', "Croatian"),
    ('hu', "Hungarian"),
    ('it', "Italian"),
    ('nl', "Dutch"),
    ('no', "Norwegian"),
    ('pl', "Polish"),
    ('pt', "Portuguese"),
    ('ro', "Romanian"),
    ('ru', "Russian"),
    ('sk', "Slovakian"),
    ('sr', "Serbian"),
    ('sv', "Swedish"),
    ('tr', "Turkish"),
    ('uk', "Ukrainian"),
    ('zh', "Chinese"),
)



# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = BASE_DIR + '/testsite/test-data/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

STATIC_URL = "/static/"

MEDIABROWSER_USER_PASSES_TEST = lambda x:True

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'mediabrowser.urls'

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'easy_thumbnails',
    'mediabrowser',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    }
]
