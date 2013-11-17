from django.conf.urls import patterns, url


urlpatterns = patterns('mediabrowser.views',
    url('^images/$', 'image_list_view', name='mediabrowser-image-list'),
    url('^images/add/$', 'image_add_view', name='mediabrowser-add-image'),
    
    url('^documents/$', 'document_list_view', name='mediabrowser-document-list'),
    url('^documents/images/$', 'image_as_document_list_view', name='mediabrowser-image-document-list'),
    url('^documents/add/$', 'document_add_view', name='mediabrowser-add-document'),
    
    url('^delete/$', 'asset_delete_view', name='mediabrowser-delete'),
)