from .models import Config, Resource, Environment
from .edcutils import getAllResource, getResourceDef, createResource, getReusableScannerConfig
import json

def edc_get_all_resources(env):
        # valid - return the jsom
        rc, tAllres = getAllResource(env.url,env.username, env.password)
        if rc==200:
            allres = []
            for tres in tAllres:
                res = Resource() 
                res.resource_name = tres['resourceName']
                res.resource_type_name = tres['resourceTypeName']
                res.resource_orig_config = env.name
                #rc, res.resource_config = getResourceDef(env.url,env.username, env.password, res.resource_name)
                allres.append(res)
            
            return allres
        else:
            return None



def edc_get_resource(env,resourceName):
     res = Resource()
     rc, j = getResourceDef(env.url,env.username, env.password, resourceName, True)
     if rc==200:
          res.resource_config=json.dumps(j)
          res.resource_name = j['resourceIdentifier']['resourceName']
          res.resource_type_name = j['resourceIdentifier']['resourceTypeName']
          res.resource_orig_config = env.name

          return res    
     else:
          return None


def edc_deploy_resource(env,res,reuse_conf):
    j=json.loads(res.resource_config)
    for config in j['scannerConfigurations']:
        if 'reusableConfigs' in config:
            for rconf in config['reusableConfigs']:
                rconf['name'] = reuse_conf
    return createResource(env.url,env.username, env.password, res.resource_name, j)
    

def edc_get_reusableconfigs(env):
     rc, j = getReusableScannerConfig(env.url,env.username, env.password)
     if rc==200:
          return json.dumps(j)
     else:
          return None
