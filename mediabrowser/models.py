from PIL import Image
from django.db import models
from django.conf import settings
import os.path
from .constants import MEDIABROWSER_UPLOAD_TO, ASSET_TYPE_CHOICES

import re

_ = lambda x:x

class Asset(models.Model):
    name = models.TextField(_("name"), max_length=120)
    file = models.FileField(_("file"), upload_to=MEDIABROWSER_UPLOAD_TO)
    type = models.CharField(_("type"), max_length=16, choices=ASSET_TYPE_CHOICES)
    ext = models.CharField(_("type"), max_length=40)
    uploaded_on = models.DateTimeField(_("uploaded on"), auto_now_add=True)
    uploaded_by = models.CharField(_("uploaded by"), max_length=80, blank=True)
    width = models.PositiveIntegerField(_("width"), blank=True, null=True)
    height = models.PositiveIntegerField(_("height"), blank=True, null=True)

    
    def save(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        if request and not self.uploaded_by:
            self.uploaded_by = unicode(request.user)
            
        if not self.name:
            m = re.search(r'([^/]+)$', self.file.url)
            self.name = m.group(1)
            self.name = re.sub(r'(_|-|%20)+', ' ', self.name)
            
        if not self.ext:
            m = re.search(r'(\w+)$', self.name)
            if m:
                self.ext = m.group(1).lower()
            
        if self.ext in ('png','jpg','jpeg','gif'):
            # we treat tiff, bmp and other image types as documents
            self.type = "img"
        else:
            self.type = "doc"
        
        resize_to = None
        img = None
        
        if self.type == "img" and not self.id:
            self.file.open('rb')
            img = Image.open(self.file)
            (imgW, imgH) = img.size
            max_size = getattr(settings, "MEDIABROWSER_MAX_IMAGE_SIZE", None)
            if max_size:
                if imgW > max_size[0] or imgH > max_size[1]:    
                    ratio = max(float(imgW)/max_size[0], float(imgH)/max_size[1])
                    resize_to = (int(imgW/ratio), int(imgH/ratio))
            
            if resize_to:
                self.width, self.height = resize_to
            else:
                self.width, self.height = img.size
        
        super(Asset, self).save(*args, **kwargs)
        
        if resize_to and img:
            img.resize(resize_to, Image.ANTIALIAS).save(self.file.path, img.format)
    
    def __unicode__(self):
        if self.type == "img":
            return '%s, %d x %d' % (self.name, self.width, self.height)
        return self.name
