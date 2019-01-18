from django.contrib import admin

# Register your models here.


from .models import Config, Resource, Environment

admin.site.register(Config)
admin.site.register(Resource)
admin.site.register(Environment)
