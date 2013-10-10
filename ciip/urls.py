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
    url(r'^upload_file/$', views.upload_file, name='upload_file'),
    url(r'^send_email/$', views.send_email, name='send_email'),
    url(r'^motivational_questions/$', views.motivational_questions, name='motivational_questions'),
    url(r'^edit_motivational_questions/$', views.edit_motivational_questions, name='edit_motivational_questions'),
    url(r'^academic_info/$', views.academic_info, name='academic_info'),
    url(r'^edit_academic_info/$', views.edit_academic_info, name='edit_academic_info'),
 
)

