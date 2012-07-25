# -*- coding: utf-8 -*-
from django.db import models
from widgets.models import Zone

class Article(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    is_active = models.BooleanField(default=False)

    zone = models.OneToOneField(Zone, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.id == None:
            zone = Zone()
            zone.save()
            self.zone = zone
        super(Article, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.zone.delete()
        super(Article, self).delete(*args, **kwargs)    
