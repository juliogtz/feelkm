from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()


#from rest_framework import routers
#from rest_framework.urlpatterns import format_suffix_patterns
#router = routers.DefaultRouter()
#router.register(r'usrs',api.views.UserViewSet)
#router.register(r'groups',api.views.GroupViewSet)

from api import *
from websearch import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'FeelKm.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$','websearch.views.LandingWeb'),
    #url(r'^',include(router.urls)),
    #url(r'^events/$','api.views.event_list'),
    #url(r'^search/$','api.views.search'),
    url(r'^admin/', include(admin)),
    # websearch
    url(r'^search/','websearch.views.SearchWeb'),

    #url(r'^(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT}),
    (r'^statics/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT}),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

    # Autocomplete Search URL
    url(r'^auto-complete/$','api.views.autocomplete'),
    url(r'^auto-complete-big/$','api.views.autocomplete_second'),


    # Register Ajax
    url(r'^register-new-user/$','usrs.views.Register'),
    # Login Ajax
    url(r'^login/$','usrs.views.LoginGo'),
    # Logout
    url(r'^logout/$','usrs.views.LogoutUser'),
    # Recovery Ajax
    url(r'^recovery/$','usrs.views.RecoveryPassword'),
    # Register Ajax Facebook Validate
    url(r'^facebook-register/$','usrs.views.Facebook_Register'),
    # Specific Event
    url(r'^[^/]+/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/[^/]+/[^/]+/(?P<id>\d+)/$','websearch.views.SepecificEvent'),
    # Example: http://www.feelkm.com/Pais/2014/04/21/Running/Nevent/2322.html replacestr
    # New Comment Event
    url(r'^[^/]+/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/[^/]+/[^/]+/(?P<id>\d+)/New-Comment/$','websearch.views.NewCommentEvent'),

    # Crear New Comment
    url(r'^create-comment/$','websearch.views.CreateComment'),
    url(r'^send-form-new-comment/$','websearch.views.CreateCommentSend'),

    #Profile User:
    url(r'^km/(?P<username>.*)/$','usrs.views.MyProfile'),


    #Privacy and Legal Information
    url(r'^privacy/$','usrs.views.Privacy'),


)

#urlpatterns = format_suffix_patterns(urlpatterns)
