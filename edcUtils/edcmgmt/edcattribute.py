from .models import Environment, Resource, Attributes
from .edcutils import getCatalogCustomAttr, createAttribute
import json

def edc_get_all_custom_attr(env):
     rj = getCatalogCustomAttr(env.url,env.username, env.password)
     attrs = []
     if rj:
         for o in rj:
              a = _attr_create_from_json(env,o)
              attrs.append(a)

         return attrs
     else:
         return None


def edc_get_custom_attr(env, attr_name):
     rj = getCatalogCustomAttr(env.url,env.username, env.password)
     a = Attributes()
     if rj:
         for o in rj:
             if attr_name == o['name']:
                  a = _attr_create_from_json(env,o)
     return a
                  


def _attr_create_from_json(e,o):
     a = Attributes()
     a.attr_id = o['id']
     a.name = o['name']
     a.description = o['description']
     a.datatypeid = o['dataTypeId']
     a.multivalued = o['multivalued']  
     a.suggestable = o['suggestable']
     a.sortable = o['sortable']
     a.searchable = o['searchable']
     a.facetable = o['facetable']
     #a.analyzer = o['analyzer']
     a.attr_config = json.dumps(o)
     a.attr_orig_env = e.name

     return a


def edc_deploy_attribute(env,attr):
     print(attr.attr_config)
     j=json.loads(attr.attr_config)
     
     data = {}
     data['items'] = []
     data['items'].append(j)

     return createAttribute(env.url,env.username, env.password, data)
