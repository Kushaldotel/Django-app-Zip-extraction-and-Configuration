
from django.urls import path,include
from pkg_resources import iter_entry_points
import importlib

from django.urls import re_path as url

urlpatterns = []

#for entry_point in iter_entry_points('assetmanagement.plugins'):
for enty_point in iter_entry_points(group='myproject', name=None):
        if importlib.util.find_spec(enty_point.module_name+'.urls'):
            urlmod = importlib.import_module(enty_point.module_name +'.urls')
            urlpatterns += [
                   path('', include((urlmod.urlpatterns,enty_point.module_name))),
            ]
            
