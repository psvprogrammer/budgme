# -*- coding: utf-8 -*-
"""
Definition of views.
"""

import os
import codecs
import copy

from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.views import View

from django.contrib.auth.models import Group
# from app.forms import ClientProfileForm, UserProfileForm, EmployeeProfileForm,\
#     GeneralAppForm
# from app.models import Client, ClientCategory, Mark, Employee, ApplicationType

from django.core.exceptions import ObjectDoesNotExist
# from django.template import RequestContext
# from django_ajax.decorators import ajax
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import activate, get_language_info


def home(request):
    return render(request, 'budgme/home.html')


def profile(request):
    return render(request, 'budgme/profile.html')


class ProfileView(LoginRequiredMixin, View):
    """docstring for Profile."""
    def get(self, request, *args, **kwargs):
        return render(request, 'budgme/profile.html')

    def post(self, request, *args, **kwargs):
        context = {
            'test_message': _('Changes saved successfuly!'),
        }
        print(request.POST)
        return render(request, 'budgme/profile.html', context)
