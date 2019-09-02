from django.conf.urls import url
from . import views
from django.contrib.auth import views as v

app_name='account'

urlpatterns = [
    url(r'^login/$', v.login, name='login'),
    url(r'^logout/$', v.logout, name='logout'),
    url(r'^logout-then-login/$', v.logout_then_login, name='logout_then_login'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^password-change/$', v.password_change, {'post_change_redirect':'account:password_change_done'}, name='password_change'),
    url(r'password-change/done', v.password_change_done, name='password_change_done'),
    url(r'^password-reset/$', v.password_reset, {"post_reset_redirect":'account:password_reset_done'}, name='password_reset'),
    url(r'^password-reset/done/$', v.password_reset_complete, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
    v.password_reset_confirm, {"post_reset_redirect":'account:password_reset_complete'}, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', v.password_change_done, name='password_reset_complete'),
    url(r'^register/$', views.register, name='register'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^users/$', views.user_list, name='user_list'),
    url(r'^users/follow/$', views.user_follow, name='user_follow'),
    url(r'^users/(?P<username>[-\w]+)/$', views.user_detail, name='user_detail'),
]