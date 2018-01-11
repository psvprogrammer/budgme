# -*- coding: utf-8 -*-
"""
Definition of views.
"""

import os
import codecs
import copy

from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.views import View
from django.views.generic import TemplateView, ListView

from django.contrib.auth.models import Group
# from app.forms import ClientProfileForm, UserProfileForm, EmployeeProfileForm,\
#     GeneralAppForm
# from app.models import Client, ClientCategory, Mark, Employee, ApplicationType

from django.core.exceptions import ObjectDoesNotExist
# from django.template import RequestContext

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q


from django.utils.translation import ugettext_lazy as _
from django.utils.translation import activate, get_language_info
# from django_ajax.mixin import AJAXMixin
from django_ajax.decorators import ajax

from budgme.models import Budget, IncomeCategory, Profile

COOKIE_DECORATORS = [
    login_required,

]


def get_current_budget(request):
    """This method return current budget object for current user
    based on session cookies"""
    budget = request.session.get('budget')
    if not budget:
        budget = Profile.objects.get(user=request.user).default_budget
        request.session['budget'] = budget.name
    else:
        budget = Budget.objects.filter(Q(owner=request.user) &
                                       Q(name=budget)).first()
    return budget


@method_decorator(COOKIE_DECORATORS, name='check_cookie')
class CheckCookieMixin:
    def check_cookie(self, request, *args, **kwargs):
        pass


# def home(request):
#     return render(request, 'budgme/home.html')


class Home(TemplateView):
    template_name = 'budgme/home.html'


def profile(request):
    return render(request, 'budgme/profile.html')


class ProfileView(CheckCookieMixin, View):
    """docstring for Profile."""
    def get(self, request, *args, **kwargs):
        return render(request, 'budgme/profile.html')

    def post(self, request, *args, **kwargs):
        context = {
            'test_message': _('Changes saved successfuly!'),
        }
        print(request.POST)
        return render(request, 'budgme/profile.html', context)


class IncomeCategories(LoginRequiredMixin, ListView):
    """Get & Post income categories page"""
    template_name = 'budgme/income/in_cat.html'

    def get_queryset(self, *args, **kwargs):
        budget = get_current_budget(self.request)
        return IncomeCategory.objects.filter(budget=budget)

@ajax
@login_required
def add_income_category(request):
    pass

@ajax
@login_required
def edit_income_category(request):
    return {}
