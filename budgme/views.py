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
from django.conf import settings

from django.contrib.auth.models import Group
# from app.forms import ClientProfileForm, UserProfileForm, EmployeeProfileForm,\
#     GeneralAppForm
# from app.models import Client, ClientCategory, Mark, Employee, ApplicationType

from django.core.exceptions import ObjectDoesNotExist
# from django.template import RequestContext
# from django_ajax.decorators import ajax
from django.db.models import Q


def home(request):
    return render(request, 'budgme/home.html')