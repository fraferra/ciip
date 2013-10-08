from django.conf.urls import patterns, url

from ciip import views

urlpatterns = patterns('',
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login ,name='login'),
    url(r'^notactive/$', views.notactive, name='notactive'),
    url(r'^notregistered/$', views.notregistered, name='notregistered'),
    url(r'^edit_contact_info/$', views.edit_contact_info, name='edit_contact_info'),
    url(r'^profile_contact_info/$', views.profile_contact_info, name ='profile_contact_info'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^home/$', views.home, name='home'),
    url(r'^eligibility/$', views.eligibility, name='eligibility'),
    #url(r'^upload_file/$', views.upload_file, name='upload_file'),
    url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    (r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^reset/(?P[0-9A-Za-z]+)-(?P.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
   # (r'^admin/(.*)', admin.site.root),

)

