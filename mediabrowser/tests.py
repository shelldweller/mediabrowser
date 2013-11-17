from django.test import TestCase
from django.test.client import Client
import os

class StickyUrlParamsTestCase(TestCase):
    def test_sticky_params_redirect(self):
        """ Test that redirect contains the original GET params. """
        
        c = Client()
        
        filepath = os.path.join(os.path.dirname(__file__), 'static', 'mediabrowser', 'img', 'test.png')
        with open(filepath) as fp:
            response = c.post('/files/add/?type=Images&CKEditor=editor2&CKEditorFuncNum=2&langCode=de', {"file":fp})
        
        url = response['Location']
        self.assertTrue('type=Images' in url)
        self.assertTrue('CKEditor=editor2' in url)
        self.assertTrue('CKEditorFuncNum=2' in url)
        self.assertTrue('langCode=de' in url)
    