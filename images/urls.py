from django.conf.urls import url
from . import views

app_name = 'images'

urlpatterns = [
    url(r'^$', views.image_list, name='list'),
    url(r'^create/$', views.image_create, name='create'),
    url(r'^detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.image_detail, name='detail'),
    url(r'^like/$', views.image_like, name='like'),
    url(r'^ranking/$', views.image_ranking, name='create'),
]
