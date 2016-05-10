from django.conf.urls import url
from . import views


urlpatterns = [
    url('^images/$', views.image_list_view , name='mediabrowser-image-list'),
    url('^images/add/$', views.image_add_view, name='mediabrowser-add-image'),
    
    url('^documents/$', views.document_list_view, name='mediabrowser-document-list'),
    url('^documents/images/$', views.image_as_document_list_view, name='mediabrowser-image-document-list'),
    url('^documents/add/$', views.document_add_view, name='mediabrowser-add-document'),
    
    url('^delete/$', views.asset_delete_view, name='mediabrowser-delete'),
]
