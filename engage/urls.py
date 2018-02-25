"""engage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from root.views import EmailViewSet, SignUp, index
from root.app.views import (
    EmailGroupSetup,
    app_index,
    email_group_detail,
    ExperimentSetup,
    TemplateSetup,
    TemplateEdit
)

router = routers.DefaultRouter()
router.register(r'emails', EmailViewSet, base_name='api-email')

app_urls = [
    url(r'^email_group_setup', EmailGroupSetup.as_view(), name='email-group-setup'),
    url(r'^email_group/(?P<pk>[0-9a-f]{32})/', email_group_detail, name='email-group-detail'),
    url(r'^experiment_setup', ExperimentSetup.as_view(), name='experiment-setup'),
    url(r'^template/setup', TemplateSetup.as_view(), name='template-setup'),
    url(r'^template/(?P<pk>[0-9a-f]{32})/', TemplateEdit.as_view(), name='template-edit'),
    url(r'^', app_index, name='index')
]

urlpatterns = [
    url(r'^auth/signup', SignUp.as_view(), name='signup'),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^app/', include(app_urls, namespace='app')),
    url(r'^', index, name='index')
]
