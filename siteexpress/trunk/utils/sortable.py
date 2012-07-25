from django.db import models
from django.db.models import F

class SortableModel(models.Model):
    """ 
    Abstract model which makes an inherited model's records sortable
    by calling instance.move(position)
    """
    order = models.IntegerField(default=0, editable=False)

    # List of fields which isolates orderings in subsets.
    # For example, if there is "parent" field, order must be
    # calculated for objects having same parent.
    order_isolation_fields = None

    class Meta:
        abstract = True
        ordering = ['order']

    def save(self, *args, **kwargs):
        """ 
        Assigns last order to position if it doesn't have an order already
        """
        try:
            if not self.order or self.order == 0:
                isolation_filters = self._calc_isolation_filters()
                last = self._get_class().objects                       \
                                     .filter(**isolation_filters)   \
                                     .values('order')               \
                                     .order_by('-order')[0]

                self.order = last['order'] + 1 
        except IndexError:
            self.order = 1
        finally:
            super(SortableModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """ 
        Decreases order for items with greater order on delete
        """
        isolation_filters = self._calc_isolation_filters()
        try:
            last = self._get_class().objects                           \
                                 .filter(**isolation_filters)       \
                                 .values('order')                   \
                                 .order_by('-order')[0]['order']
        except IndexError:
            super(SortableModel, self).delete(*args, **kwargs)
            return

        super(SortableModel, self).delete(*args, **kwargs)            
        self._get_class().objects                                  \
                      .filter(**isolation_filters)              \
                      .filter(order__range=(self.order, last))  \
                      .update(order=F('order')-1)

    def move(self, to):
        """ 
        Moves item to given position
        """
        to = int(to)
        if to < 1:
            to = 1

        orig = self.order
        if to == orig:
            return
     
        isolation_filters = self._calc_isolation_filters()
        last = self._get_class().objects                         \
                             .filter(**isolation_filters)     \
                             .values('order')                 \
                             .order_by('-order')[0]['order']

        if to > last:
            to = last

        shift, range = to < orig and (1, (to, orig-1)) or (-1, (orig+1, to))
        self._get_class().objects                          \
                      .filter(**isolation_filters)      \
                      .filter(order__range=range)       \
                      .update(order=F('order')+shift)
     
        self.order = to
        self.save()
    
    def _get_class(self):
        return self.__class__
    
    def _calc_isolation_filters(self): 
        """ 
        Returns a dict with arguments to pass to .filter()
        to isolate ordering calculations
        """   
        isolation_filters = {}
        if self.order_isolation_fields is not None:
            for field in self.order_isolation_fields:
                isolation_filters[field] = self.__getattribute__(field)

        return isolation_filters
