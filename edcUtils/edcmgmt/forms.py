from django import forms

from .models import Config,Environment

class ConfigForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Config
        fields = ('config_name', 'edc_version', 'url', 'username', 'password', 'security_domain',)


class EnvironmentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class=form-control': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class=form-control': True}))
    
    edc_version = forms.ChoiceField(label='EDC Version', widget=forms.Select(attrs={'class=form-control': True}),choices=Environment.ENV_VERSIONS)
    url = forms.CharField(label='URL', widget=forms.TextInput(attrs={'class=form-control': True}), max_length=255)
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class=form-control': True}),max_length=30) 
    security_domain = forms.CharField(label='Security Domain', widget=forms.TextInput(attrs={'class=form-control': True}), max_length=30) 

    class Meta:
        model = Environment
        fields = ('name', 'edc_version', 'url', 'username', 'password', 'security_domain',)
