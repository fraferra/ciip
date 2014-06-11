from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from ciip import views

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='info/', permanent=False), name='index'),
    #url(r'send_email/^$', RedirectView.as_view(url='contact_us/', permanent=False), name='index'),
    #url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup/$', views.info, name='info'),
    url(r'^login/$', views.login ,name='login'),
    url(r'^notactive/$', views.notactive, name='notactive'),
    url(r'^notregistered/$', views.notregistered, name='notregistered'),
    url(r'^edit_contact_info/$', views.edit_contact_info, name='edit_contact_info'),
    #url(r'^edit_contact_info/$', views.profile_contact_info, name='profile_contact_info'),
    url(r'^profile_contact_info/$', views.profile_contact_info, name ='profile_contact_info'),

    url(r'^logout/$', views.logout, name='logout'),
    url(r'^home/$', views.home, name='home'),
    url(r'^eligibility/$', views.eligibility, name='eligibility'),
    url(r'^upload_file/$', views.upload_file, name='upload_file'),
    url(r'^upload_visa/$', views.upload_visa, name='upload_visa'),
    url(r'^send_email/$', views.send_email, name='send_email'),

    url(r'^motivational_questions/$', views.motivational_questions, name='motivational_questions'),
    url(r'^edit_motivational_questions/$', views.edit_motivational_questions, name='edit_motivational_questions'),
    #url(r'^edit_motivational_questions/$', views.motivational_questions, name='motivational_questions'),

    url(r'^academic_info/$', views.academic_info, name='academic_info'),
    url(r'^edit_academic_info/$', views.edit_academic_info, name='edit_academic_info'),
    #url(r'^edit_academic_info/$', views.academic_info, name='academic_info'),
    #url(r'^upload_image/$', views.upload_image, name='upload_image'),
    url(r'^info/$', views.info, name='info'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^contact_us/$', views.contact_us, name='contact_us'),

    url(r'^skill_interest/$', views.skill_interest, name='skill_interest'),
    url(r'^edit_skill_interest/$', views.edit_skill_interest, name='edit_skill_interest'),
    #url(r'^edit_skill_interest/$', views.skill_interest, name='skill_interest'),


    url(r'^alternative_sign_up/$', views.alternative_sign_up, name='alternative_sign_up'),
    url(r'^intern_profiles/$', views.intern_profiles, name='intern_profiles'),
    url(r'^video/$', views.video, name='video'),

    url(r'^work_internship/$', views.work_internship, name='work_internship'),
    url(r'^edit_work_internship/$', views.edit_work_internship, name='edit_work_internship'),
    #url(r'^edit_work_internship/$', views.work_internship, name='work_internship'),

    url(r'^cover_letter/$', views.cover_letter, name='cover_letter'),
    url(r'^current_project/$', views.current_project, name='current_project'),
    url(r'^interview/$', views.interview, name='interview'),
    url(r'^my_managers/$', views.my_managers, name='my_managers'),
    url(r'^student_send_message/$', views.student_send_message, name='student_send_message'),











    url(r'^home_uniadmin/$', views.home_uniadmin, name='home_uniadmin'),
    url(r'^uniadmin_info/$', views.uniadmin_info, name='uniadmin_info'),
    url(r'^uniadmin_edit_info/$', views.uniadmin_edit_info, name='uniadmin_edit_info'),
    url(r'^uniadmin_login/$', views.uniadmin_login ,name='uniadmin_login'),
    url(r'^list_student/$', views.list_student ,name='list_student'),
    url(r'^student_info/$', views.student_info ,name='student_info'),
    url(r'^signup_uniadmin/$', views.signup_uniadmin, name='signup_uniadmin'),
    url(r'^save_unicomment/$', views.save_unicomment, name='save_unicomment'),


    url(r'^manager_history/$', views.manager_history, name='manager_history'),
    url(r'^manager_signup/$', views.manager_signup, name='manager_signup'),
    url(r'^manager_login/$', views.manager_login, name='manager_login'),
    url(r'^manager_home/$', views.manager_home, name='manager_home'),
    url(r'^manager_logout/$', views.manager_logout, name='manager_logout'),
    #url(r'^result/$', views.result, name='result'),
    url(r'^schedule_interview/$', views.schedule_interview, name='schedule_interview'),
    url(r'^my_students/$', views.my_students, name='my_students'),
    url(r'^manager_send_message/$', views.manager_send_message, name='manager_send_message'),
    url(r'^manager_info/$', views.manager_info, name='manager_info'),
    url(r'^manager_edit_info/$', views.manager_edit_info, name='manager_edit_info'),
    url(r'^student_full_profile/$', views.student_full_profile, name='student_full_profile'),
    url(r'^manager_guidelines/$', views.manager_guidelines, name='manager_guidelines'),
    url(r'^downloads/$', views.downloads, name='downloads'), 




)

