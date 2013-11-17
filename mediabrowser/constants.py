from django.conf import settings

MEDIABROWSER_UPLOAD_TO = getattr(settings, 'MEDIABROWSER_UPLOAD_TO', "mb/%Y/%m")

MEDIABROWSER_PAGE_SELECTOR_URL = getattr(settings, 'MEDIABROWSER_PAGE_SELECTOR_URL', None)

MEDIABROWSER_USER_PASSES_TEST = getattr(settings, 'MEDIABROWSER_USER_PASSES_TEST',
                                         lambda user:user.is_staff)

ASSET_TYPE_CHOICES = (
    ('img', 'Image'),
    ('doc', 'Document'),
)