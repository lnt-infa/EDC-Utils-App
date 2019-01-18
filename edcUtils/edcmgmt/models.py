from django.db import models

# Create your models here.

class Config(models.Model):
    config_name = models.CharField(max_length=50)
    version = models.CharField(max_length=15)
    edc_version = models.CharField(max_length=15)
    url = models.CharField(max_length=255)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    security_domain = models.CharField(max_length=50)
    resource_count = models.IntegerField(default=0)
    object_count = models.IntegerField(default=0)

class Environment(models.Model):
    ENV_VERSIONS=(
      ('10.1.0', '10.1'),
      ('10.1.1','10.1.1'),
      ('10.2.0', '10.2'),
      ('10.2.1', '10.2.1'),
      ('10.2.2', '10.2.2'),
    )
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=15)
    edc_version = models.CharField(max_length=15,choices=ENV_VERSIONS)
    url = models.CharField(max_length=255)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    security_domain = models.CharField(max_length=50)
    resource_count = models.IntegerField(default=0)
    object_count = models.IntegerField(default=0)
    custom_attr_count = models.IntegerField(default=0)
    
class Resource(models.Model):
    resource_name = models.CharField(max_length=255)
    resource_config = models.TextField()
    resource_type_name = models.CharField(max_length=255,default='-')
    resource_orig_config = models.CharField(max_length=50, default='-')
    resource_env_version = models.CharField(max_length=15, blank=True)

class Attributes(models.Model):
    attr_id = models.CharField(max_length=255, default='-')
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    datatypeid = models.CharField(max_length=255)
    multivalued = models.BooleanField()
    suggestable = models.BooleanField()
    sortable = models.BooleanField()
    searchable = models.BooleanField()
    facetable = models.BooleanField()
    analyzer = models.CharField(max_length=255)
    attr_config = models.TextField()
    attr_orig_env = models.CharField(max_length=50, default='-')
    attr_env_version = models.CharField(max_length=15, blank=True)
    
