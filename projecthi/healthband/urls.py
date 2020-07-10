from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    index, signinform, submitLogin, loggedin, patient, regform, register, UserRegistration, providerRegistration, providerRegistration, saveSettings, logoutuser,viewPatientData
    )
from django.contrib.auth import views as auth_views

app_name = 'healthband'
urlpatterns = [
            url(r'^$', index, name='index'),
            url(r'^signinform/$', signinform, name='signinform'),
            url(r'^login/$', submitLogin, name='submitLogin'),
            url(r'^signout/', auth_views.logout),
            url(r'^signin/loggedin/$', loggedin, name='loggedin'),
            #view of patient data
            url(r'^viewpatientdata/$', viewPatientData, name='viewPatientData'),
            #registration form
            url(r'^regform/$', regform, name='regform'),

            #submit registration form
            url(r'^register/$', register, name="register"),
            url(r'^register2/$', UserRegistration, name="UserRegistration"),
            url(r'^providerregistration/$', providerRegistration, name="providerRegistration"),
            
            #submit patient settings form
            url(r'^saveSettings/$', saveSettings, name="saveSettings"),
            url(r'^logout/$', logoutuser, name="logoutuser")
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
