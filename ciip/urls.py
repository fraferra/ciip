from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from ciip import views

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='info/', permanent=False), name='index'),
    #url(r'send_email/^$', RedirectView.as_view(url='contact_us/', permanent=False), name='index'),
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
    #url(r'^upload_image/$', views.upload_image, name='upload_image'),
    url(r'^info/$', views.info, name='info'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^contact_us/$', views.contact_us, name='contact_us'),
    url(r'^skill_interest/$', views.skill_interest, name='skill_interest'),
    url(r'^edit_skill_interest/$', views.edit_skill_interest, name='edit_skill_interest'),
    url(r'^alternative_sign_up/$', views.alternative_sign_up, name='alternative_sign_up'),
    url(r'^intern_profiles/$', views.intern_profiles, name='intern_profiles'),
    url(r'^video/$', views.video, name='video'),
    url(r'^work_internship/$', views.work_internship, name='work_internship'),
    url(r'^edit_work_internship/$', views.edit_work_internship, name='edit_work_internship'),
    url(r'^cover_letter/$', views.cover_letter, name='cover_letter'),

)

