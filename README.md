Media browser for Django.

Setup
-----

In settings.py:

```python
# add mediabrowser to INSTALLED_APPS:
INSTALLED_APPS = (
    ...
    'mediabrowser',
    ...
)

# Optional settings:

# Where mediabrowser should upload files (default is "mb/%Y/%m"):
MEDIABROWSER_UPLOAD_TO = "mb/%Y/%m"

# URL for selecting links in your CMS.
# If set, this vlaue will be passed to {% url %} template tag:
MEDIABROWSER_PAGE_SELECTOR_URL = "my-cms-url-content-selector-name"

# Function for user access to mediabrowser
# (defaults is user.is_staff)
MEDIABROWSER_USER_PASSES_TEST = lambda user:user.is_authenticated
```

In urls.py:
```python
urlpatterns = patterns('',
    ...
    url(r'', include('mediabrowser.urls')),
    ...
)
```

After having added ```mediabrowser``` to ```INSTALLED_APPS``` run ```./manage.py syncdb```.



Controlling mediabrowser access
-------------------------------

By default media browser access is allowed for any authenticated user. If this is not
what you need you could do one of the following:

* Set ```MEDIABROWSER_USER_PASSES_TEST```. It should be a callable that takes user object as argument
and returns boolean. It is a single acces control option for uploading, browsing and deletion.
* Manually decorate class views inside your own URL conf.


Integrating your CMS content browser
------------------------------------

To integrate mediabrowser with your custom CMS to be able to select your CMS's content
to link to, do the following:

* Define your own view listing content.
* Set ```MEDIABROWSER_PAGE_SELECTOR_URL``` to url name of this view.
* Make your view's template inherit from ```mediabrowser/base.html```.
(Required context variables: asset_type=doc, page_selector_url=<your_url>)

Subclass ```mediabrowser.views.BaseAssetListView``` or create your own view with
the following to template context:

```python
context = {
    # media browser needs to retain original query string set by the editor:
    'QUERY_STRING': self.request.GET.urlencode(),
    
    # set asset_type to doc to use mediabrowser in link mode (as apposed to image insertion mode),
    # otherwise "Browse documents" and "Browse content" tabs won't appear:
    "asset_type": "doc",
    
    # Editor needs to know your page_selector_url, otherwise it will not display the
    # "Browse content" tab:
    "page_selector_url": settings.MEDIABROWSER_PAGE_SELECTOR_URL
    
    'QUERY_STRING': request.GET.urlencode(),
}
```

Customizing appearance
----------------------

To override CSS definitions create your own ```mediabrowser/includes/css.html``` and include your own CSS.

By default mediabrowser uses [easy-thumbnails](https://github.com/SmileyChris/easy-thumbnails). If you
would like to use your own thumbnailing engine override ```mediabrowser/includes/asset-listing.html```.



WYSIWYG integration
-------------------

By default mediabrowser is designed to work with CKEdit. Integrating it with another editor
should be fairly easy. Just provide your own function for inserting files:

```javascript
MEDIABROWSER.insertFile = function(asset_url) {
    // handle asset insertion here
}
```

This can be done inside your own ```mediabrowser/includes/head.html``` include file.

Note that you don't need to close editor window from your custom fuction. This will be done
automatically after your funciton is executed.
