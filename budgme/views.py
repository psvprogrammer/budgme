# -*- coding: utf-8 -*-
"""
Definition of views.
"""

# import os
# import codecs
# import copy

from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.views import View
from django.views.generic import TemplateView, ListView, FormView
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import Group

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


# Bootstrap sizes according to it's grid system
XS_SIZE = 768
MD_SIZE = 992
LG_SIZE = 1200


def get_grid_size(request):
    """This method parses client size window based on
    bootstrap grid system and returns one of the string:
    'xs' - if width < 768px
    'sm' - if width >= 768px
    'md' - if width >= 992px
    'lg' - if width >= 1200px
    default is 'lg'
    """
    try:
        width = int(request.GET.get('width'))
    except:
        return 'lg'
    else:
        if width >= LG_SIZE:
            return 'lg'
        elif width >= MD_SIZE:
            return 'md'
        elif width >= XS_SIZE:
            return 'sm'
        else:
            return 'xs'


def profile(request):
    return render(request, 'budgme/profile.html')


class MasterPage(TemplateView):
    template_name = 'budgme/master.html'


class BaseAjaxRenderer:
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


class IncomeCategories(BaseAjaxRenderer):
    """All Get & Post CRUD operations for income categories urls"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form = forms.IncomeCategoryForm

    def ajax_income_categories(self):

        def get_queryset(request):
            budget = get_current_budget(request)
            return IncomeCategory.objects.filter(budget=budget)

        context = {
            'object_list': get_queryset(self.request),
            'grid_size': get_grid_size(self.request),
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
        form = self.form(self.request.POST)
        if form.is_valid():
            if not self._name_unique(form.cleaned_data.get('name')):
                return
            try:
                category = IncomeCategory.objects.get(
                    id=self.request.POST['id'], budget=self.budget)
            except ObjectDoesNotExist:
                self._fail_popover(msg=__('Can not find this category in DB!'))
                return

            for field in form.cleaned_data:
                setattr(category, field, form.cleaned_data.get(field))
            category.save()
            self._success_popover()
        else:
            self._fail_popover(msg=form.errors.as_text())

    def ajax_add_in_cat(self):
        form = self.form(self.request.POST)
        if form.is_valid():
            if not self._name_unique(form.cleaned_data.get('name')):
                return
            category = IncomeCategory(
                budget=self.budget,
                name=form.cleaned_data.get('name'),
                description=form.cleaned_data.get('description'))
            try:
                category.save()
            except Exception as why:
                self._fail_popover(msg=str(why))
                return
            else:
                row_context = {
                    'income_category': category,
                }
                self.append_content = [
                    ("table#table-in_cat>tbody",
                     render(self.request,
                            'budgme/income/in_cat_row.html',
                            row_context)),
                ]
                self._success_popover(msg=__('New income source added'))
        else:
            self._fail_popover(title=__('Failed to add new resource!'),
                               msg=form.errors.as_text())

    def ajax_del_in_cat(self):
        pass

    def _name_unique(self, name):
        self.budget = get_current_budget(self.request)
        category_name_exist = IncomeCategory.objects.filter(
            Q(budget=self.budget) &
            Q(name=name) &
            ~Q(id=self.request.POST['id'])).count() > 0
        if category_name_exist:
            self._fail_popover(
                msg=__('Name must be unique for this budget!'))
            return False
        else:
            return True

    def _fail_popover(self, title=__('Error'),
                      msg=__('Fail to save your changes'), errors={}):
        if errors:
            try:
                msg += '\n'
                for field, error in errors.items():
                    msg += '- ' + field + ': ' + error[0] + '\n'
            except:
                msg += '\n' + str(errors)
        self.response.update({
            'success': False,
            'title': title,
            'content': msg,
            'template': render(
                self.request, 'budgme/popovers/popover_error.html'),
        })

    def _success_popover(self, title=__('Success'),
                         msg=__('Your changes saved!')):
        self.response.update({
            'success': True,
            'title': title,
            'content': msg,
            'template': render(
                self.request, 'budgme/popovers/popover_success.html'),
        })


AjaxViews = (
    IncomeCategories,
)


class AJAXRenderer(*AjaxViews, AJAXMixin, LoginRequiredMixin, View):

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

