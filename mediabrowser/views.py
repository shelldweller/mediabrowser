from django.views.generic import ListView, CreateView, View
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.utils.translation import activate
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.http import QueryDict, HttpResponse
import json

try:
    from urllib.parse import urlsplit, urlunsplit
except ImportError:     # Python 2
    from urlparse import urlsplit, urlunsplit


from .models import Asset
from .forms import AssetForm
from .constants import MEDIABROWSER_PAGE_SELECTOR_URL, MEDIABROWSER_USER_PASSES_TEST

_ = lambda x:x

def auth_required(function, perm=None):
    """
    If settings.MEDIABROWSER_CHECK_USER_PERMISSIONS is set to True and perm is not None,
    will verify user permissions. Otherwise will validate user access via
    settings.MEDIABROWSER_USER_PASSES_TEST
    """
    def check_perm(user):
        if perm and getattr(settings, "MEDIABROWSER_CHECK_USER_PERMISSIONS", False):
            if user.has_perm(perm):
                return True
            raise PermissionDenied
        else:
            return MEDIABROWSER_USER_PASSES_TEST(user)
    return user_passes_test(check_perm)(function)


class LocaleActivationMixing(object):
    """ Activates locale based on query string parameter. """
    def dispatch(self, request, *args, **kwargs):
        lang = request.GET.get("langCode", None)
        if lang:
            activate(lang)
        return super(LocaleActivationMixing, self).dispatch(request, *args, **kwargs)


class StickyGetParamsMixin(object):
    """ Mixin that persists GET params between requests. """
    
    def get_success_url(self):
        """ Updates success URL with GET params. """
        url = super(StickyGetParamsMixin, self).get_success_url()
        scheme, netloc, path, query, fragment = urlsplit(url)
        get_params = QueryDict(query, mutable=True)
        get_params.update(self.request.GET)
        return urlunsplit((scheme, netloc, path, get_params.urlencode(), fragment))
    
    def get_context_data(self, *args, **kwargs):
        """ Adds QUERY_STRING to context variable. """
        context = super(StickyGetParamsMixin, self).get_context_data(*args, **kwargs)
        context['QUERY_STRING'] = self.request.GET.urlencode()
        context['page_selector_url'] = MEDIABROWSER_PAGE_SELECTOR_URL
        if getattr(settings, "MEDIABROWSER_CHECK_USER_PERMISSIONS", False):
            context['can_upload'] = self.request.user.has_perm('mediabrowser.add_asset')
            context['can_delete'] = self.request.user.has_perm('mediabrowser.delete_asset')
        else:
            context['can_upload'] = True
            context['can_delete'] = True

        return context
    

class JsonResponseMixin(object):
    def response(self, data):
        return HttpResponse(json.dumps(data), content_type="application/json")


class AssetTypeMixin(object):
    asset_type = None # set by subclass

    def get_context_data(self, *args, **kwargs):
        context = super(AssetTypeMixin, self).get_context_data(*args, **kwargs)
        context['asset_type'] = getattr(self, 'context_asset_type', self.asset_type)
        return context


class BaseAssetListView(LocaleActivationMixing, StickyGetParamsMixin, AssetTypeMixin, ListView):
    template_name = "mediabrowser/list.html"
    model = Asset
    context_object_name = "assets"
    
    def get_queryset(self):
        return Asset.objects.filter(type=self.asset_type)


class ImageListView(BaseAssetListView):
    asset_type = "img"

image_list_view = auth_required(ImageListView.as_view())


class ImageLinkListView(BaseAssetListView):
    """ View to browse images in the link context. """
    asset_type = "img"
    context_asset_type = "doc"

image_as_document_list_view = auth_required(ImageLinkListView.as_view())


class DocumentListView(BaseAssetListView):
    asset_type = "doc"

document_list_view = auth_required(DocumentListView.as_view())

class BaseAssetAddView(LocaleActivationMixing, StickyGetParamsMixin, CreateView):
    model = Asset
    form_class = AssetForm
    template_name = "mediabrowser/add.html"
    template_name_success = "mediabrowser/add_success.html"
    
    def form_valid(self, form):
        """ Renders response that inserts asset into caller's editor. """
        self.object = form.save(commit=False)
        self.object.uploaded_by = unicode(self.request.user)
        self.object.save()
        
        return self.response_class(
            request = self.request,
            template = self.template_name_success,
            context = {"asset":self.object}
        )


class ImageAddView(AssetTypeMixin, BaseAssetAddView):
    asset_type = "img"
    
image_add_view = auth_required(ImageAddView.as_view(), "mediabrowser.add_asset")


class DocumentAddView(AssetTypeMixin, BaseAssetAddView):
    asset_type = "doc"
    
document_add_view = auth_required(DocumentAddView.as_view(), "mediabrowser.add_asset")



class AssetDeleteView(LocaleActivationMixing, JsonResponseMixin, View):
    def post(self, request):
        return self.delete(request)
    
    def delete(self, request):
        try:
            asset_id = int(request.POST.get("asset_id"))
        except ValueError:
            return self.response({"status":"error", "message":_("Please select a file to be deleted.")})
        try:
            asset = Asset.objects.get(id=asset_id)
        except Asset.DoesNotExist:
            return self.response({"status":"error", "message":_("Invalid asset id.")})
        asset.delete()
        return self.response({"status":"ok", "id":asset_id})

asset_delete_view = auth_required(AssetDeleteView.as_view(), "mediabrowser.delete_asset")

