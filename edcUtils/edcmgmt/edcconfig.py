from .models import Config, Resource
from .edcutils import getAllResource, getResourceDef, getCatalogResourceCount, getCatalogObjectCount

def edc_get_resource_count(config):
     rc, rj = getCatalogResourceCount(config.url,config.username, config.password)
     if rc==200:
         count = rj['metadata']['totalCount']
            
         return count
     else:
         return None



def edc_get_object_count(config):
     rc, rj = getCatalogObjectCount(config.url,config.username, config.password)
     if rc==200:
         count = rj['metadata']['totalCount']
            
         return count
     else:
         return None
