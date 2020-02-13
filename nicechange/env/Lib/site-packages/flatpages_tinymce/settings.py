import os
from django.conf import settings

# Use TinyMCE in admin area
USE_ADMIN_AREA_TINYMCE = getattr(settings, "FLATPAGES_TINYMCE_ADMIN", True)
# Use TinyMCE on frontend
USE_FRONTED_TINYMCE = getattr(settings, "FLATPAGES_TINYMCE_FRONTEND", True)

# Directory with flatpages templates
TEMPLATE_DIR = getattr(settings, "FLATPAGES_TEMPLATE_DIR", os.path.join(settings.TEMPLATE_DIRS[0], 'flatpages'))

# Regexp for flatpages template files
TEMPLATE_FILES_REGEXP = getattr(settings, 'FLATPAGES_ADMIN_REGEXP', r'.*\.d?html?$')

# Prefix for auto-generated html elements
DIV_PREFIX = getattr(settings, 'FLATPAGES_DIV_PREFIX', "django_staticpages_edit")

# Use minified versions of javascript and css files
USE_MINIFIED = getattr(settings, 'FLATPAGES_USE_MINIFIED', None)
if USE_MINIFIED is None:
    USE_MINIFIED = not getattr(settings, 'DEBUG')

if 'staticfiles' in settings.INSTALLED_APPS:
    MEDIA_URL = os.path.join(getattr(settings, 'STATIC_URL', ''), 'flatpages_tinymce')
else:
    MEDIA_URL = getattr(settings, 'FLATPAGES_MEDIA_URL', os.path.join(settings.MEDIA_URL, 'flatpages_tinymce'))
