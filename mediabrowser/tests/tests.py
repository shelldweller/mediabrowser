from django.test import TestCase, override_settings
from django.test.client import Client
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image

import os



IMAGE_ROOT = os.path.join(os.path.dirname(__file__), 'test-data')


class AuthenticatedUserTestCase(TestCase):
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

    
class FileBrowsingTestCase(AuthenticatedUserTestCase):
    
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


class FileUploadTestCase(AuthenticatedUserTestCase):
    
    def test_image_upload(self):
        c = self.get_client()
        filepath =  os.path.join(IMAGE_ROOT, '40x40.png')
        with open(filepath) as fp:
            response = c.post('/images/add/?type=Images&CKEditor=editor2&CKEditorFuncNum=2&langCode=de', {"file":fp})        
        filepath =  os.path.join(IMAGE_ROOT, '40x40.png')
        self.assertTrue("asset" in response.context)
        self.uploaded.append(response.context["asset"].file.path)
        self.assertTrue("MEDIABROWSER.insertFile" in response.content, "Missing MEDIABROWSER.insertFile call in response")
    
    
    @override_settings(MEDIABROWSER_MAX_IMAGE_SIZE=(500,500))
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
        
