from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from tappsi_api.viewsets import UserViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'user', UserViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tappsi_test.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
