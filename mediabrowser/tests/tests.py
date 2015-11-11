from django.test import TestCase, override_settings
from django.test.client import Client
from django.contrib.auth.models import User, Permission
from django.conf import settings
from django.core.urlresolvers import reverse
from PIL import Image

from mediabrowser.models import Asset

import os



IMAGE_ROOT = os.path.join(os.path.dirname(__file__), 'test-data')


class AuthenticatedUserBaseTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user("testuser", password="s3kret")
        user.is_staff = True
        user.save()
        self.uploaded = []
    
    def tearDown(self):
        for f in self.uploaded:
            os.remove(f)
    

    def get_client(self):
        c = Client()
        c.login(username="testuser", password="s3kret")
        return c

    
class FileBrowsingTestCase(AuthenticatedUserBaseTestCase):
    
    def test_sticky_params_in_links(self):
        """ Test that file browser links contains the original GET params. """
        params = {
            "type": "Images",
            "CKEditor": "editor2",
            "CKEditorFuncNum": "2",
            "langCode": "en",
        }
        url = '/images/add/'
        c = self.get_client()
        response = c.get(url, params)
        # we should really parse HTML and extract links instad of this:
        for k,v in params.items():
            self.assertContains(response, k+"="+v)


class FileUploadTestCase(AuthenticatedUserBaseTestCase):
    
    @override_settings(MEDIABROWSER_CHECK_USER_PERMISSIONS=None)
    def test_image_upload(self):
        c = self.get_client()
        filepath =  os.path.join(IMAGE_ROOT, '40x40.png')
        with open(filepath) as fp:
            response = c.post('/images/add/?type=Images&CKEditor=editor2&CKEditorFuncNum=2&langCode=de', {"file":fp})        
        filepath =  os.path.join(IMAGE_ROOT, '40x40.png')
        self.assertTrue("asset" in response.context)
        self.uploaded.append(response.context["asset"].file.path)
        self.assertTrue("MEDIABROWSER.insertFile" in response.content, "Missing MEDIABROWSER.insertFile call in response")
    
    
    @override_settings(MEDIABROWSER_MAX_IMAGE_SIZE=(500,500), MEDIABROWSER_CHECK_USER_PERMISSIONS=None)
    def test_image_resizing(self):
        client = self.get_client()
        
        # 40x40.png should not be resized, it's small
        filepath =  os.path.join(IMAGE_ROOT, '40x40.png')
        with open(filepath) as fp:
            response = client.post('/images/add/?type=Images', {"file":fp})
        orig_img = Image.open(filepath)
        uploaded_img = Image.open(response.context["asset"].file.path)
        self.assertEqual(orig_img.size[0], uploaded_img.size[0])
        self.assertEqual(orig_img.size[1], uploaded_img.size[1])
        
        # 600x600.png should be resized to 500x500
        filepath =  os.path.join(IMAGE_ROOT, '600x600.png')
        with open(filepath) as fp:
            response = client.post('/images/add/?type=Images', {"file":fp})
        asset = response.context["asset"]
        uploaded_img = Image.open(asset.file)
        self.uploaded.append(response.context["asset"].file.path)
        
        self.assertEqual(500, asset.width)
        self.assertEqual(500, asset.height)
        self.assertEqual(500, uploaded_img.size[0])
        self.assertEqual(500, uploaded_img.size[1])


class AuthenticationTestCase(AuthenticatedUserBaseTestCase):
    def post_image(self):
        filepath =  os.path.join(IMAGE_ROOT, '40x40.png')
        client = self.get_client()
        with open(filepath) as fp:
            response = client.post('/images/add/?type=Images', {"file":fp})
        return response
    
    def update_user_perms(self, *codenames):
        user = User.objects.get(username="testuser")
        for codename in codenames:
            user.user_permissions.add(Permission.objects.get(codename=codename, content_type__app_label="mediabrowser"))
        
    @override_settings(MEDIABROWSER_CHECK_USER_PERMISSIONS=True, MEDIABROWSER_USER_PASSES_TEST=None)
    def test_require_user_permissions(self):
        """ Tests that if MEDIABROWSER_CHECK_USER_PERMISSIONS=True, user must have valid permissions to add or delete assets. """
        
        # by default user has no add_asset permission so request should be denied
        response = self.post_image()
        self.assertEqual(response.status_code, 403)
        
        # + add_asset permission
        self.update_user_perms("add_asset")
        response = self.post_image()
        self.assertEqual(response.status_code, 200)
        
        # deleting an asset should result in 403 because user has no delete perm
        asset = Asset.objects.all().order_by("-id")[0]
        url = reverse("mediabrowser-delete")
        response = self.get_client().post(url, {"asset_id":asset.id})
        self.assertEqual(response.status_code, 403)
        
        # + delete_asset permission and now we can delete
        self.update_user_perms('delete_asset')
        response = self.get_client().post(url, {"asset_id":asset.id})
        self.assertEqual(response.status_code, 200)
    
    @override_settings(MEDIABROWSER_CHECK_USER_PERMISSIONS=None, MEDIABROWSER_USER_PASSES_TEST=None)
    def test_default_user_permissions(self):
        """ Tests that default user permissions allow adding and deleting assets. """
        
        # upload image
        response = self.post_image()
        self.assertEqual(response.status_code, 200)
        
        # delete image
        asset = Asset.objects.all().order_by("-id")[0]
        url = reverse("mediabrowser-delete")
        response = self.get_client().post(url, {"asset_id":asset.id})
        self.assertEqual(response.status_code, 200)
    
    @override_settings(MEDIABROWSER_CHECK_USER_PERMISSIONS=None, MEDIABROWSER_USER_PASSES_TEST=None)
    def test_template_with_default_permissions(self):
        """ Tests that with default user permissions upload and delete buttons are present. """
        upload_url = reverse("mediabrowser-add-image")
        response = self.get_client().get(reverse("mediabrowser-image-list"))
        self.assertIn(upload_url, response.content)
        self.assertIn('id="DeleteFile"', response.content)
    
    @override_settings(MEDIABROWSER_CHECK_USER_PERMISSIONS=True, MEDIABROWSER_USER_PASSES_TEST=None)
    def test_template_with_default_permissions(self):
        """ Tests delete and upload links are only present if user has apropriate permissions. """
        upload_url = reverse("mediabrowser-add-image")
        
        # if user has no permission, delete and upload links should not be there
        response = self.get_client().get(reverse("mediabrowser-image-list"))
        self.assertNotIn(upload_url, response.content)
        self.assertNotIn('id="DeleteFile"', response.content)
        
        # after updating permissions, both links should become visible
        self.update_user_perms("add_asset", "delete_asset")
        response = self.get_client().get(reverse("mediabrowser-image-list"))
        self.assertIn(upload_url, response.content)
        self.assertIn('id="DeleteFile"', response.content)
        
    
    