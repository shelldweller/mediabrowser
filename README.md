Media browser for Django.

# Setup


By default mediabrowser uses [easy-thumbnails](https://github.com/SmileyChris/easy-thumbnails)
for creating image thumbnails.

In settings.py:

```python
# add mediabrowser to INSTALLED_APPS:
INSTALLED_APPS = (
    ...
    'easy_thumbnails',
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
# (defaults to user.is_staff)
MEDIABROWSER_USER_PASSES_TEST = lambda user:user.is_authenticated

# Require mediabrowser to check user permissions
# (defaults to False)
MEDIABROWSER_CHECK_USER_PERMISSIONS = True

# Automatically resize uploaded images to fit within given dimensions
# (default to None, i.e. no resizing)
MEDIABROWSER_MAX_IMAGE_SIZE = (800, 400)
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



# Controlling mediabrowser access

By default full media browser access is allowed for any authenticated staff user
(i.e., ```user.is_staff == True```). You can use the following settings to refine user access
rules:

Set ```MEDIABROWSER_USER_PASSES_TEST```. It should be a callable that takes user object as argument
and returns Boolean. It is a single access control option for uploading, browsing and deletion. Example:

```python
MEDIABROWSER_USER_PASSES_TEST = lambda user: user.has_perm("mycms.change_content")
```

Set ```MEDIABROWSER_CHECK_USER_PERMISSIONS = True```. This will ensure user must have
explicit permissions to delete or add assets.


# Integrating your CMS content browser

To integrate mediabrowser with your custom CMS to be able to select your CMS's content
to link to, do the following:

* Define your own view listing content.
* Set ```MEDIABROWSER_PAGE_SELECTOR_URL``` to url name of this view.
* Make your view's template inherit from ```mediabrowser/base.html```.
(Required context variables: asset_type=doc, page_selector_url=*your_url*)

You CMS integration view can be created by subclassing
```mediabrowser.views.BaseAssetListView```. But you can also create your view from scratch.
Just pass the following context to the template:

```python
context = {
    # mediabrowser needs to retain original query string set by the editor:
    'QUERY_STRING': self.request.GET.urlencode(),
    
    # set asset_type to doc to use mediabrowser in link mode
    # (as apposed to image insertion mode),
    # otherwise "Browse documents" and "Browse content" tabs won't appear:
    "asset_type": "doc",
    
    # Editor needs to know your page_selector_url, otherwise it will not display the
    # "Browse content" tab:
    "page_selector_url": settings.MEDIABROWSER_PAGE_SELECTOR_URL
}
```

# Customizing appearance

To override CSS definitions create your own ```mediabrowser/includes/css.html``` and include your own CSS.

By default mediabrowser uses [easy-thumbnails](https://github.com/SmileyChris/easy-thumbnails). If you
would like to use your own thumbnailing engine override ```mediabrowser/includes/asset-listing.html```.



# WYSIWYG integration


## CKEditor

In Django template:

```html
<script>
    // To activate image broswer:
    CKEDITOR.config.filebrowserImageBrowseUrl = "{% url 'mediabrowser-add-image' %}";
    
    // To activate file browser:
    CKEDITOR.config.filebrowserLinkBrowseUrl = "{% url 'mediabrowser-add-document' %}";
</script>
```

For details see [CKEditor documentation](http://docs.ckeditor.com/#!/api/CKEDITOR.config-cfg-filebrowserImageBrowseUrl).

## Custom integration

```javascript
MEDIABROWSER.insertFile = function(asset_url) {
    // handle asset insertion here
}
```

This can be done inside your own ```mediabrowser/includes/head.html``` include file.

Note that you don't need to close editor window from your custom fuction. This will be done
automatically after your funciton is executed.
