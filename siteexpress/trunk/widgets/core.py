from django.db import models
from django.db.models.query import QuerySet

class SubclassingQuerySet(QuerySet):
    """ QuerySet extension for getting derived class instances instead of base """
    def __getitem__(self, k):
        result = super(SubclassingQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model):
            return result.as_leaf_class()
        else:
            return result
    def __iter__(self):
        for item in super(SubclassingQuerySet, self).__iter__():
            yield item.as_leaf_class()

class WidgetManager(models.Manager):
    pass

class WidgetLeafManager(models.Manager):
    """ Manager, based on SubclassingQuerySet """
    def get_query_set(self):
        return SubclassingQuerySet(self.model)