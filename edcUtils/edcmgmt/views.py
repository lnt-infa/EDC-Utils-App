'''
Created on Dec 28, 2018

Views for the EDC Env Manager app

@author: lntrapad
'''

from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404,redirect

from .models import Resource, Environment, Attributes
from .forms import EnvironmentForm
from .edcresource import edc_get_all_resources,edc_get_resource, edc_deploy_resource,edc_get_reusableconfigs
from .edcenvironment import edc_get_resource_count,edc_get_object_count,edc_get_custom_attr_count
from .edcattribute import edc_get_custom_attr,edc_get_all_custom_attr, edc_deploy_attribute

from io import  StringIO
import json

def index(request):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    view for the main index page redirecting to the login or environment page

    @return HTML

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if request.user.is_authenticated:
      #template = loader.get_template('base.html')
      #context = {}
      #return HttpResponse(template.render(context, request))
      return redirect('Env')
    else:
      return redirect('login')


def envs(request):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    view of the list of environment already present in the DB

    @return HTML
     
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')
    
    all_env=Environment.objects.all()
    for env in all_env:
      if env.object_count == 0 or env.resource_count == 0 or env.custom_attr_count == 0:
        env.object_count=edc_get_object_count(env)
        env.resource_count=edc_get_resource_count(env)
        env.custom_attr_count=edc_get_custom_attr_count(env)
        env.save()

    template = loader.get_template('environment/index.html')
    context = {
       'all_env': all_env,
    }

    return HttpResponse(template.render(context, request))


def new_env(request):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    view for new environment creation
    
    @return HTML

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')

    if request.method == "POST":
      form = EnvironmentForm(request.POST)
      if form.is_valid():
        env = form.save(commit=False)
        _save_env(env)
      return redirect('Env')
    else:
      form = EnvironmentForm()
      return render(request,'environment/new.html',{'form':form})

def _save_env(env):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    when saving the environment object, update it with counts of object/attrbutes , etc.

    @return None
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    env.object_count=edc_get_object_count(env)
    env.resource_count=edc_get_resource_count(env)
    env.custom_attr_count=edc_get_custom_attr_count(env)

    env.save()    
    return


def env(request, env_id):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    view to display the detail of an environement
    @arg: env_id, id of the environment instance
    
    @return HTML

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')

    env = get_object_or_404(Environment, pk=env_id)
    return render(request,'environment/detail.html',{'env':env})


def edit_env(request, env_id):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    view to edit the detail of an environement
    @arg: env_id, id of the environment instance
     
    if form submitted, environment detail are saved into DB and page is redirected to list of env
    
    @return HTML

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')

    env = get_object_or_404(Environment, pk=env_id)
    form = EnvironmentForm(request.POST or None, instance=env)
    if form.is_valid():
        env=form.save(commit=False)
        _save_env(env)
        return redirect('Env')
    return render(request,'environment/new.html',{'form':form})

def del_env(request,env_id):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    view to handle env deletion
    
    @return HTML

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')
    Environment.objects.filter(id=env_id).delete() 

    return redirect('Env')


def resource_ext_all(request):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    view to retieve and display all resource of an environment
    @arg: env_id, is passed using the POST method

    @return HTML
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')
    if request.method == "POST":
        return _resource_ext(request,request.POST['env_id'])
    else:
        return _resource_ext(request,None)

def resource_ext(request, env_id):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    view to retieve and display all resource of an environment
    @arg: env_id, is passed using the GET method

    @return HTML
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')
    return _resource_ext(request, env_id)

def _resource_ext(request,env_id):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    retieve and display all resource of an environment
    
    @return HTML

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    all_env=Environment.objects.all()

    saved_resources = Resource.objects.all()

    template = loader.get_template('resource/external.html')

    if env_id:
        env = get_object_or_404(Environment, pk=env_id)
        resources = edc_get_all_resources(env)
        context = {
          'all_env': all_env,
          'env': env,
          'resources': resources,
        }
    else:
        context = {
          'all_env': all_env,
        }
    return HttpResponse(template.render(context, request))


def resource_saved(request,previousMessage=None): 
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    retieve and display all resource defintion saved in the DB

    @return HTML
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')
    all_env=Environment.objects.all()
    saved_resources = Resource.objects.all()

    template = loader.get_template('resource/saved.html')
    context = {
          'all_env': all_env,
          'saved_resources' : saved_resources,
          'previousMessage' : previousMessage,
    }
    return HttpResponse(template.render(context, request))




def resource_detail(request,env_id,resource_name): 
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    retieve and display detail of a resource from environment in parameter

    @return HTML
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')
    template = loader.get_template('resource/detail.html')
    
    resource=edc_get_resource(get_object_or_404(Environment, pk=env_id),resource_name)
    json_pretty=json.dumps(json.loads(resource.resource_config),indent=4) 

    context = {
      'resource': resource,
      'json_pretty' : json_pretty,
    }

    return HttpResponse(template.render(context, request))



def resource_export(request,env_id,resource_name):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    handle exporting resource to a file

    @return json file

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')

    resource=edc_get_resource(get_object_or_404(Environment, pk=env_id),resource_name)

    tFile=StringIO(json.dumps(resource.resource_config,indent=4, sort_keys=True))

    response = HttpResponse(tFile.getvalue(),content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="'+resource_name+'.json"'

    return response

def resource_save(request,env_id,resource_name):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    handle saving resource defintion to the DB

    @return HTML

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')

    resource=edc_get_resource(get_object_or_404(Environment, pk=env_id),resource_name)
    resource.resource_env_version = get_object_or_404(Environment, pk=env_id).edc_version
    
    resource.save()
    return redirect('res-saved')

def resource_del(request, res_id):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    handle deletion of a resource defintion from the DB

    @return HTML

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')
    Resource.objects.filter(id=res_id).delete() 

    return redirect('res-saved')

def resource_deploy(request):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    handle deployment of a resource to another environment

    @return HTML

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')
    
    if request.method == "POST":
       env=get_object_or_404(Environment, pk=request.POST['env_id'])
       res=get_object_or_404(Resource,  pk=request.POST.get('res_id',None)) 
       reuse_conf=request.POST.get('reuse_conf',None)
       rc, j = edc_deploy_resource(env,res,reuse_conf) 
       if rc == 200:
           return redirect('res-ext',env_id=request.POST['env_id'])
       else:
           return resource_saved(request,j['message'])          

def resource_deploy_checks(request,env_id,res_id):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    perfom checks before deployment of a resource to another environment
    this view is called via AJAX

    @return JSON

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')
 
    env=get_object_or_404(Environment, pk=env_id)
    res=get_object_or_404(Resource, pk=res_id) 

    r= {}
    if env.edc_version != res.resource_env_version:
        r['code']="001"
        r['message']="Environment and resource definition are not on same version"
        
    else:
        r['code']="000"

    return JsonResponse(r)


def _attributes_ext(request,env_id):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    all_env=Environment.objects.all()

    template = loader.get_template('attribute/external.html')
    if env_id:
        env = get_object_or_404(Environment, pk=env_id)
        attributes = edc_get_all_custom_attr(env)
        context = {
          'all_env': all_env,
          'env': env,
          'attributes': attributes,
        }
    else:
        context = {
          'all_env': all_env,
        }

    return HttpResponse(template.render(context, request))


def attributes_ext(request, env_id):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    retrieve and display all custom attribute of an environment
    env_id is passed using GET method

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')
     
    return _attributes_ext(request,env_id)

def attributes_ext_all(request):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    retrieve and display all custom attribute of an environment
    env_id is passed using POST method

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')
    if request.method == "POST":
        return _attributes_ext(request,request.POST['env_id'])
    else:
        return _attributes_ext(request,None)

def attribute_ext_detail(request,env_id,attr_name): 
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    display detail of a custom attribute from an environment

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')

    template = loader.get_template('attribute/detail.html')
    
    attr=edc_get_custom_attr(get_object_or_404(Environment, pk=env_id),attr_name)
    json_pretty=json.dumps(json.loads(attr.attr_config),indent=4) 

    context = {
      'attr': attr,
      'json_pretty' : json_pretty,
    }

    return HttpResponse(template.render(context, request))

def attributes_save(request,env_id,attr_name):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    handle saving an attribute defintion to the DB

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')

    attr=edc_get_custom_attr(get_object_or_404(Environment, pk=env_id),attr_name)
    attr.attr_env_version = get_object_or_404(Environment, pk=env_id).edc_version
    
    attr.save()
    return redirect('attr-saved')

def attributes_saved(request,previousMessage=None):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    display all attribute save in the DB
    take previousMessage as optional parameter to be display in red in the rendered page in case of error

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')

    all_env=Environment.objects.all()
    saved_attributes = Attributes.objects.all()

    template = loader.get_template('attribute/saved.html')
    context = {
        'all_env': all_env,
        'saved_attributes': saved_attributes,
        'previousMessage' : previousMessage,
    }

    return HttpResponse(template.render(context, request))

def attributes_del(request, attr_id):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    handle delection of an attribute from the DB

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')

    Attributes.objects.filter(id=attr_id).delete() 

    return redirect('attr-saved')

def attributes_deploy(request):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    handle deployment of a saved attribute to another enviromnent

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')
    
    if request.method == "POST":
       env=get_object_or_404(Environment, pk=request.POST['env_id'])
       attr=get_object_or_404(Attributes,  pk=request.POST.get('attr_id',None)) 
       # check if the target env has the same version as the atrribute definition
       rc, j = edc_deploy_attribute(env,attr) 
       if rc == 200:
           return redirect('attr-ext',env_id=request.POST['env_id'])
       else:
           return attributes_saved(request,j['message'])


def attributes_deploy_checks(request,env_id,attr_id):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    perform checks before deploying attribute

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')
 
    env=get_object_or_404(Environment, pk=env_id)
    attr=get_object_or_404(Attributes, pk=attr_id) 

    r= {}
    if env.edc_version != attr.attr_env_version:
        r['code']="001"
        r['message']="Environment and attribute definition are not on same version"
        
    else:
        r['code']="000"

    return JsonResponse(r)

def attributes_export(request,env_id,attr_name):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    handle export of the attribute definition as a file

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')

    attr=edc_get_custom_attr(get_object_or_404(Environment, pk=env_id),attr_name)

    tFile=StringIO(json.dumps(attr.attr_config,indent=4, sort_keys=True))

    response = HttpResponse(tFile.getvalue(),content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="'+attr_name+'.json"'

    return response


def reusableconfig(request,env_id):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    retrive reusable configs from an enviornment
    this view is called via AJAX
 
    @return JSON

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if not request.user.is_authenticated:
      return redirect('login')

    env=get_object_or_404(Environment, pk=env_id)
    return HttpResponse(edc_get_reusableconfigs(env))
