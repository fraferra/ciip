from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from ciip.views import *

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='info/', permanent=False), name='index'),
    #url(r'send_email/^$', RedirectView.as_view(url='contact_us/', permanent=False), name='index'),
    #url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup/$', views_students.signup, name='info'),
    url(r'^login/$', views_students.login ,name='login'),
    url(r'^notactive/$', views_general.notactive, name='notactive'),
    url(r'^notregistered/$', views_general.notregistered, name='notregistered'),


    url(r'^edit_contact_info/$', views_students.edit_contact_info, name='edit_contact_info'),
    url(r'^profile_contact_info/$', views_students.profile_contact_info, name ='profile_contact_info'),

    url(r'^logout/$', views_students.logout, name='logout'),
    url(r'^home/$', views_students.home, name='home'),
    url(r'^eligibility/$', views_general.eligibility, name='eligibility'),
    url(r'^upload_file/$', views_students.upload_file, name='upload_file'),
    url(r'^upload_visa/$', views_students.upload_visa, name='upload_visa'),
    url(r'^send_email/$', views_students.send_email, name='send_email'),

    url(r'^motivational_questions/$', views_students.motivational_questions, name='motivational_questions'),
    url(r'^edit_motivational_questions/$', views_students.edit_motivational_questions, name='edit_motivational_questions'),
    #url(r'^edit_motivational_questions/$', views.motivational_questions, name='motivational_questions'),

    url(r'^academic_info/$', views_students.academic_info, name='academic_info'),
    url(r'^edit_academic_info/$', views_students.edit_academic_info, name='edit_academic_info'),
    #url(r'^edit_academic_info/$', views.academic_info, name='academic_info'),
    #url(r'^upload_image/$', views.upload_image, name='upload_image'),
    url(r'^info/$', views_general.info, name='info'),
    url(r'^faq/$', views_general.faq, name='faq'),
    url(r'^contact_us/$', views_general.contact_us, name='contact_us'),

    url(r'^skill_interest/$', views_students.skill_interest, name='skill_interest'),
    url(r'^edit_skill_interest/$', views_students.edit_skill_interest, name='edit_skill_interest'),
    #url(r'^edit_skill_interest/$', views.skill_interest, name='skill_interest'),


    url(r'^alternative_sign_up/$', views_students.alternative_sign_up, name='alternative_sign_up'),
    url(r'^intern_profiles/$', views_general.intern_profiles, name='intern_profiles'),
    url(r'^video/$', views_general.video, name='video'),

    url(r'^work_internship/$', views_students.work_internship, name='work_internship'),
    url(r'^edit_work_internship/$', views_students.edit_work_internship, name='edit_work_internship'),
    #url(r'^edit_work_internship/$', views.work_internship, name='work_internship'),

    url(r'^cover_letter/$', views_students.cover_letter, name='cover_letter'),
    url(r'^current_project/$', views_general.current_project, name='current_project'),
    url(r'^interview/$', views_students.interview, name='interview'),
    url(r'^my_managers/$', views_students.my_managers, name='my_managers'),
    url(r'^student_send_message/$', views_students.student_send_message, name='student_send_message'),











    url(r'^home_uniadmin/$', views_uniadmins.home_uniadmin, name='home_uniadmin'),
    url(r'^uniadmin_info/$', views_uniadmins.uniadmin_info, name='uniadmin_info'),
    url(r'^uniadmin_edit_info/$', views_uniadmins.uniadmin_edit_info, name='uniadmin_edit_info'),
    url(r'^uniadmin_login/$', views_uniadmins.uniadmin_login ,name='uniadmin_login'),
    url(r'^list_student/$', views_uniadmins.list_student ,name='list_student'),
    url(r'^student_info/$', views_uniadmins.student_info ,name='student_info'),
    url(r'^signup_uniadmin/$', views_uniadmins.signup_uniadmin, name='signup_uniadmin'),
    url(r'^save_unicomment/$', views_uniadmins.save_unicomment, name='save_unicomment'),


    url(r'^manager_history/$', views_managers.manager_history, name='manager_history'),
    url(r'^manager_signup/$', views_managers.manager_signup, name='manager_signup'),
    url(r'^manager_login/$', views_managers.manager_login, name='manager_login'),
    url(r'^manager_home/$', views_managers.manager_home, name='manager_home'),
    url(r'^manager_logout/$', views_managers.manager_logout, name='manager_logout'),
    #url(r'^result/$', views.result, name='result'),
    url(r'^schedule_interview/$', views_managers.schedule_interview, name='schedule_interview'),
    url(r'^my_students/$', views_managers.my_students, name='my_students'),
    url(r'^manager_send_message/$', views_managers.manager_send_message, name='manager_send_message'),
    url(r'^manager_info/$', views_managers.manager_info, name='manager_info'),
    url(r'^manager_edit_info/$', views_managers.manager_edit_info, name='manager_edit_info'),
    url(r'^student_full_profile/$', views_managers.student_full_profile, name='student_full_profile'),
    url(r'^manager_guidelines/$', views_managers.manager_guidelines, name='manager_guidelines'),
    url(r'^downloads/$', views_managers.downloads, name='downloads'), 




)

