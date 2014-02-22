from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

import os



IMAGE_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testsite', 'img')


class AuthenticatedUserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user("testuser", password="s3kret")
        user.is_staff = True
        user.save()
    
    def cleanUp(self):
        #TODO: delete all uploaded images
        pass
    

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
        filepath =  os.path.join(IMAGE_ROOT, 'test.png')
        with open(filepath) as fp:
            response = c.post('/images/add/?type=Images&CKEditor=editor2&CKEditorFuncNum=2&langCode=de', {"file":fp})
        self.assertTrue("asset" in response.context)
        self.assertTrue("MEDIABROWSER.insertFile" in response.content, "Missing MEDIABROWSER.insertFile call in response")
