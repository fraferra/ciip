from django.conf.urls import patterns, include, url
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ciip/', include('ciip.urls', namespace="ciip")),
    url(r'^$', RedirectView.as_view(url='ciip/', permanent=False), name='index'),


    url(r'^forgot_password/$', 'django.contrib.auth.views.password_reset', {'template_name' : 'ciip/forgot_password.html'}, name='forgot_password'),
    
    url(r'^forgot_password_confirm/(?P<uidb36>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect' : '/forgot_password_done/'},
        name='forgot_password_confirm'),

    url(r'^forgot_password_done/$', 'django.contrib.auth.views.password_reset_done', name='forgot_password_done')



)


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
