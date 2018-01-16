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
from django.views.generic import TemplateView, ListView, FormView
from django.shortcuts import get_object_or_404

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
from django.utils.translation import ugettext as __
from django.utils.translation import activate, get_language_info
from django_ajax.mixin import AJAXMixin
# from django_ajax.decorators import ajax

from budgme.models import Budget, IncomeCategory, Profile
from budgme.forms import CustomAuthenticationForm, CustomPasswordChangeForm
from budgme import forms

# AJAX_DECORATORS = [
#     login_required,
#     ajax,
# ]


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


# @method_decorator(AJAX_DECORATORS, name='check_cookie')
class CheckCookieMixin:
    def check_cookie(self, request, *args, **kwargs):
        pass


# def home(request):
#     return render(request, 'budgme/home.html')


class Home(TemplateView):
    template_name = 'budgme/home.html'


def profile(request):
    return render(request, 'budgme/profile.html')


# class ProfileView(CheckCookieMixin, View):
#     """docstring for Profile."""
#     def get(self, request, *args, **kwargs):
#         return render(request, 'budgme/profile.html')
#
#     def post(self, request, *args, **kwargs):
#         context = {
#             'test_message': _('Changes saved successfuly!'),
#         }
#         print(request.POST)
#         return render(request, 'budgme/profile.html', context)


class IncomeCategories(LoginRequiredMixin, ListView):
    """Get & Post income categories page"""
    template_name = 'budgme/income/in_cat.html'

    def get_queryset(self, *args, **kwargs):
        budget = get_current_budget(self.request)
        return IncomeCategory.objects.filter(budget=budget)

# @ajax
# @login_required
# def add_income_category(request):
#     pass


# @method_decorator(AJAX_DECORATORS, name='post')
class EditIncomeCategoryView(View):
    def __init__(self):
        self.result = {}

    def post(self, request, *args, **kwargs):
        form = forms.EditIncomeCategoryForm(request.POST)
        if form.is_valid():
            budget = get_current_budget(request)
            category_name_exist = IncomeCategory.objects.filter(
                Q(budget=budget) &
                Q(name=form.cleaned_data.get('name')) &
                ~Q(id=request.POST['id'])).count() > 0
            if category_name_exist:
                self._fail_result(
                    msg=__('Name must be unique for this budget!'))
                # result.update({
                #     'success': False,
                #     'title': 'Error',
                #     'content': __('You already have income category with this name!'),
                #     'template': render(request, 'budgme/popovers/in_cat_error.html'),
                # })
                return self.result
            try:
                category = IncomeCategory.objects.get(
                    id=request.POST['id'], budget=budget)
            except ObjectDoesNotExist:
                self._fail_result(msg=__('Can not find this category in DB!'))
                # result.update({
                #     'success': False,
                #     'errors': __('Can not find this category in DB!'),
                # })
                return self.result

            for field in form.changed_data:
                setattr(category, field, form.cleaned_data.get(field))
            category.save()
            self._success_result()
            # result.update({
            #     'msg': __('Changes saved'),
            # })
        else:
            self._fail_result(msg=__('Check for required fields!'))
        return self.result

    def _fail_result(self, title=__('Error'),
                     msg=__('Fail to save your changes')):
        self.result.update({
            'success': False,
            'title': title,
            'content': msg,
            'template': render(
                self.request, 'budgme/popovers/in_cat_error.html'),
        })

    def _success_result(self, title=__('Success'),
                        msg=__('Your changes saved!')):
        self.result.update({
            'success': True,
            'title': title,
            'content': msg,
            'template': render(
                self.request, 'budgme/popovers/in_cat_success.html'),
        })


class MasterPage(TemplateView):
    template_name = 'budgme/master.html'


# @method_decorator(AJAX_DECORATORS, name='get')
class AJAXRenderer(AJAXMixin, LoginRequiredMixin, View):
    def __init__(self):
        """Any content passed in response must be a
        list of tuple(selector, content)"""
        self.replace_content = None
        self.main_content = None
        self.append_content = None
        self.prepend_content = None

        self.response = {
            'fragments': {
                # 'replace element with this content'
                # self.replace_content goes here
            },
            'inner-fragments': {
                # 'replace inner content'
                # self.main_content goes here
            },
            'append-fragments': {
                # 'append this content'
                # self.append_content goes here
            },
            'prepend-fragments': {
                # 'prepend this content'
                # self.prepend_content goes here
            },
        }

    def get(self, request, *args, **kwargs):
        self.render_page()
        return self.response

    def post(self, request, *args, **kwargs):
        self.render_page()
        return self.response

    def render_page(self):
        try:
            method = getattr(self, self.request.resolver_match.url_name)
            method()
        except AttributeError:
            self.page_404()
        self._update_response()

    def page_404(self):
        self.main_content = [
            ('#main-container', render(self.request, 'budgme/404.html')),
        ]

    def ajax_home(self):
        self.main_content = [
            ('#main-container', render(self.request, 'budgme/home.html')),
        ]

    def ajax_income_categories(self):

        def get_queryset(request):
            budget = get_current_budget(request)
            return IncomeCategory.objects.filter(budget=budget)

        context = {
            'object_list': get_queryset(self.request),
        }
        self.main_content = [
            ('#main-container', render(self.request,
                                       'budgme/income/in_cat.html', context)),
        ]
        self.append_content = [
            ('#scripts', render(self.request,
                                'budgme/income/in_cat_scripts.html')),
        ]

    def ajax_edit_in_cat(self):
        pass

    def _update_response(self):
        if self.replace_content:
            for selector, html in self.replace_content:
                self.response['fragments'].update({
                    selector: str(html.content).replace('\\n', '')[2:-1],
                })

        if self.main_content:
            for selector, html in self.main_content:
                self.response['inner-fragments'].update({
                    selector: str(html.content).replace('\\n', '')[2:-1],
                })

        if self.append_content:
            for selector, html in self.append_content:
                self.response['append-fragments'].update({
                    selector: str(html.content).replace('\\n', '')[2:-1],
                })

        if self.prepend_content:
            for selector, html in self.prepend_content:
                self.response['prepend-fragments'].update({
                    selector: str(html.content).replace('\\n', '')[2:-1],
                })

