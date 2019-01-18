from .models import Environment, Resource
from .edcutils import getAllResource, getResourceDef, getCatalogResourceCount, getCatalogObjectCount, getCatalogCustomAttr

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


def edc_get_custom_attr_count(config):
     rj = getCatalogCustomAttr(config.url,config.username, config.password)
     if rj:
       return len(rj)  
     else:
       return 0
