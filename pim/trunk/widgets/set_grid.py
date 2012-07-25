# -*- coding: utf-8 -*-

from django.db import models
from models import Widget, Zone
from grouping import create_group, add2group

create_group('grids', 'Сетка')

class GridWidget(Widget):

    own_template = "grid"

    GRID_CHOICES = (
        (1, '100'),
        (2, '50/50'),
        (3, '66/33'),
        (4, '33/66'),
        (5, '33/33/33'),
    )
    
    grid_type = models.PositiveIntegerField("Grid type", choices=GRID_CHOICES)

    grid_zone_1 = models.OneToOneField(Zone, related_name='grid_zone_1', 
                                  verbose_name='Zone 1', null=True, blank=True, editable=False)
    grid_zone_2 = models.OneToOneField(Zone, related_name='grid_zone_2', 
                                  verbose_name='Zone 2', null=True, blank=True, editable=False)
    grid_zone_3 = models.OneToOneField(Zone, related_name='grid_zone_3', 
                                  verbose_name='Zone 3', null=True, blank=True, editable=False)

    def columns(self):
        cols = self.type.split('_')[1:]
        remind = 0
        result = []
        for i in cols:
            j = remind
            remind = remind + int(i)
            result.append((i, j))
        return result

    def save(self, *args, **kwargs):
        if self.id is None:
            zone_1 = Zone()
            zone_1.save()
            self.grid_zone_1 = zone_1
            zone_2 = Zone()
            zone_2.save()
            self.grid_zone_2 = zone_2
            zone_3 = Zone()
            zone_3.save()
            self.grid_zone_3 = zone_3
        self.type = 'Grid_' + '_'.join(self.GRID_CHOICES[self.grid_type-1][1].split('/'))
        super(GridWidget, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.grid_zone_1.delete()
        self.grid_zone_2.delete()
        self.grid_zone_3.delete()
        super(GridWidget, self).delete(*args, **kwargs)


@add2group('100', 'grids')
class Grid_100(GridWidget):
    def save(self, *args, **kwargs):
        if (self.grid_type is None):
            self.grid_type = 1
        super(Grid_100, self).save(*args, **kwargs)
    class Meta:
        proxy = True

@add2group('50/50', 'grids')
class Grid_50_50(GridWidget):
    def save(self, *args, **kwargs):
        if (self.grid_type is None):
            self.grid_type = 2
        super(Grid_50_50, self).save(*args, **kwargs)
    class Meta:
        proxy = True

@add2group('66/33', 'grids')
class Grid_66_33(GridWidget):
    def save(self, *args, **kwargs):
        if (self.grid_type is None):
            self.grid_type = 3
        super(Grid_66_33, self).save(*args, **kwargs)
    class Meta:
        proxy = True

@add2group('33/66', 'grids')
class Grid_33_66(GridWidget):
    def save(self, *args, **kwargs):
        if (self.grid_type is None):
            self.grid_type = 4
        super(Grid_33_66, self).save(*args, **kwargs)
    class Meta:
        proxy = True

@add2group('33/33/33', 'grids')
class Grid_33_33_33(GridWidget):
    def save(self, *args, **kwargs):
        if (self.grid_type is None):
            self.grid_type = 5
        super(Grid_33_33_33, self).save(*args, **kwargs)
    class Meta:
        proxy = True
