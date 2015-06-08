#title           :pyscript.py
#description     :Extend letucce for implemented BDD on Django.
#author          :juniorgerdet
#date            :04-06-2015
#version         :0.1
#usage           :python manager harvest
#notes           :
#python_version  :2.7.10  
#==============================================================================
from django.conf.urls import patterns, include, url
from tappsi_api.views import UserViewSet, RideViewSet, AvailableView
from rest_framework.routers import DefaultRouter
from django.contrib import admin
admin.autodiscover()

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'rides', RideViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tappsi_test.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
	url(r'^api/v1/availables',  AvailableView.as_view(), name="logout"),
    url(r'^api/v1/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/docs/', include('rest_framework_swagger.urls')),

)
