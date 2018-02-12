"""budgme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static
from django.contrib import admin
from django.views.generic.base import RedirectView

from django.contrib.auth.views import login, logout,\
    password_change, password_change_done

from datetime import datetime
from budgme import views
from budgme.forms import CustomAuthenticationForm, CustomPasswordChangeForm
from django.utils.translation import ugettext_lazy as _

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login$', login,
        {
            'template_name': 'budgme/login.html',
            'authentication_form': CustomAuthenticationForm,
            'extra_context':
                {
                    'title': _('Login, please'),
                    'year': datetime.now().year,
                }
        }, name='login'),
    url(r'^logout$', logout,
        {
            'next_page': '/login'
        }, name='logout'),
    url(r'^password_change/$', password_change,
        {
            'template_name': 'budgme/password_change.html',
            'password_change_form': CustomPasswordChangeForm,
            'extra_context':
                {
                    'title': _('You can change your password')
                }
        }, name='password_change'),
    url(r'^password_change/done/$', password_change_done,
        {
            'template_name': 'app/password_change_done.html',
        }, name='password_change_done'),

    # home pages
    url(r'^$', views.MasterPage.as_view(), name='home'),
    url(r'^home$', views.MasterPage.as_view(), name='index'),
    url(r'^ajax/$', views.AJAXRenderer.as_view(), name='ajax_home'),

    # profile pages
    url(r'^profile$', views.MasterPage.as_view(), name='profile'),
    url(r'^ajax/profile$', views.AJAXRenderer.as_view(), name='ajax_profile'),

    # income category pages
    url(r'^income-categories$', views.MasterPage.as_view(), name='income_categories'),
    url(r'^ajax/income-categories$', views.AJAXRenderer.as_view(), name='ajax_income_categories'),
    url(r'^ajax/add-in-cat$', views.AJAXRenderer.as_view(), name='ajax_add_in_cat'),
    url(r'^ajax/edit-in-cat$', views.AJAXRenderer.as_view(), name='ajax_edit_in_cat'),
    url(r'^ajax/del-in-cat$', views.AJAXRenderer.as_view(), name='ajax_del_in_cat'),

    # budget pages
    url(r'^ajax/change_budget$', views.AJAXRenderer.as_view(), name='ajax_change_budget'),

    # url(r'^.*$', RedirectView.as_view(url='/', permanent=False), name='index'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if not settings.DEBUG:
#     urlpatterns += static('',
#         (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
#     )
