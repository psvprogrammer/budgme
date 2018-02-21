"""
Models Definition
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.translation import ugettext_lazy as _
from django.utils.text import format_lazy
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse


User = get_user_model()


def user_logged_in_set_default_budget_cookie(sender, request, user,
                                             *args, **kwargs):
    """Set default budget in cookie if no such cookie yet"""
    default_budget = request.session.get('budget')
    if not default_budget:
        default_budget = Profile.objects.get(user=user).default_budget.name
        request.session['budget'] = default_budget


user_logged_in.connect(user_logged_in_set_default_budget_cookie)


def user_post_save_profile_creation(sender, instance, created,
                                    *args, **kwargs):
    """Automatically creating profile for all newly created users.
    All users has to have at least one budget. Here we creating its
    first 'default' user budget.
    Plus adding this 'default' budget to BudgetAccess table
    with our user as target_user with full access
    """
    if not created:
        return

    # creating default budget
    default_budget = Budget(
        owner=instance, name='default',
        description=_('This is your first automaticatlly created '
                      'default budget')
    )
    default_budget.save()

    # creating user profile
    profile = Profile(user=instance, default_budget=default_budget)
    profile.save()


post_save.connect(user_post_save_profile_creation, sender=User)


class Budget(models.Model):
    class Meta:
        verbose_name = _('Budget')
        verbose_name_plural = _('Budgets')

    owner = models.ForeignKey(User, null=False, blank=False,
                              verbose_name=_('* Budget owner'),
                              help_text=_('Set the owner for this budget'),
                              on_delete=models.CASCADE)
    name = models.CharField(_('* Budget name'), null=False, blank=False,
                            help_text=_('Set the name of this budget'),
                            max_length=120)
    description = models.CharField(_('Description'), null=True, blank=True,
                                   help_text=_('Describe the purposes '
                                   'of this budget'), max_length=254)
    icon = models.CharField(_('Set icon for your budget'),
                            default='fa-money', blank=True, max_length=100)
    is_active = models.BooleanField(_('Is this budget is active?'), default=True)

    def get_balance(self, period):
        return str(period)

    def __str__(self):
        return str(format_lazy('{name} (owner: {owner})',
                               name=self.name, owner=self.owner))


class IncomeCategory(models.Model):
    class Meta:
        verbose_name = _('Income category')
        verbose_name_plural = _('Income categories')

    budget = models.ForeignKey(Budget, null=False, blank=False,
                               verbose_name=_('* Target budget'),
                               help_text=_('Choose target budget'),
                               on_delete=models.CASCADE)
    name = models.CharField(_('* Income category name'), null=False, blank=False,
                            help_text=_('Set the name of the category '
                                        '(should be unique in target budget)'),
                            max_length=120)
    description = models.CharField(_('Description'), null=False, blank=True,
                                   help_text=_('Describe what is for this '
                                               'income category'),
                                   max_length=254, default='')
    is_active = models.BooleanField(_('Should budget count incomes '
                                      'from this category?'), default=True)

    def __str__(self):
        return str(format_lazy('{name}, budget: {budget}',
                               name=self.name.upper(), budget=self.budget))


class OutcomeCategory(models.Model):
    class Meta:
        verbose_name = _('Outcome category')
        verbose_name_plural = _('Outcome categories')

    budget = models.ForeignKey(Budget, null=False, blank=False,
                               verbose_name=_('* Target budget'),
                               help_text=_('Choose target budget'),
                               on_delete=models.CASCADE)
    name = models.CharField(_('* Outcome category name'),
                            null=False, blank=False, max_length=120,
                            help_text=_('Set the name of the category '
                                        '(should be unique in target budget)'))
    description = models.CharField(_('Description'), null=True, blank=True,
                                   help_text=_('Describe what this '
                                               'outcome category is for'),
                                   max_length=254)
    is_active = models.BooleanField(_('Should budget count outcomes '
                                      'from this category?'), default=True)

    def __str__(self):
        return str(format_lazy('{name}, budget: {budget}',
                               name=self.name.upper(), budget=self.budget))


class Income(models.Model):
    class Meta:
        verbose_name = _('Income')
        verbose_name_plural = _('Incomes')

    user = models.ForeignKey(User, null=True, blank=False,
                             verbose_name=_('* Owner user'),
                             help_text=_('Set the user that is the owner'),
                             on_delete=models.SET_NULL)
    budget = models.ForeignKey(Budget, null=False, blank=False,
                               verbose_name=_('* Target budget'),
                               help_text=_('Choose target budget'),
                               on_delete=models.CASCADE)
    category = models.ForeignKey(IncomeCategory, null=True, blank=False,
                                 verbose_name=_('* Category'),
                                 help_text=_('Set the category '
                                             'for this income'),
                                 on_delete=models.SET_NULL)
    value = models.DecimalField(_('* Value'), null=False, blank=False,
                                help_text=_('Set the amount of new income'),
                                default=0.0, decimal_places=2, max_digits=8)
    date = models.DateTimeField(_('* Creation date'), null=False, blank=True,
                                auto_now_add=True, auto_now=False,
                                help_text=_('Set the income date'))
    description = models.CharField(_('Description'), null=True, blank=True,
                                   help_text=_('Describe what is about '
                                               'this income'),
                                   max_length=254)
    is_planned = models.BooleanField(_('Is planned'), null=False, blank=True,
                                     help_text=_('Does it planned income?'),
                                     default=False)

    def __str__(self):
        return str(format_lazy('{value}: {category}',
                               value=self.value, category=self.category))


class OutcomePlace(models.Model):
    class Meta:
        verbose_name = _('outcome place')
        verbose_name_plural = _('outcome places')

    budget = models.ForeignKey(Budget, null=True, blank=False,
                               verbose_name=_('* Target budget'),
                               help_text=_('Choose target budget'),
                               on_delete=models.SET_NULL)
    name = models.CharField(_('* Name'),
                            help_text=_('Set the name of the new place '
                                        '(should be unique)'), max_length=254)
    description = models.CharField(_('Description'), null=True, blank=True,
                                   help_text=_('Describe what is about '
                                               'this income'),
                                   max_length=254)
    location = models.CharField(_('Location'), null=True, blank=True,
                                help_text=_('Set the coordinates'),
                                max_length=254)


class OutcomePlaceCategory(models.Model):
    outcome_place = models.ForeignKey(OutcomePlace, null=True, blank=False,
                                      verbose_name=_('Place'),
                                      on_delete=models.SET_NULL)
    outcome_category = models.ForeignKey(OutcomeCategory,
                                         null=True, blank=False,
                                         verbose_name=_('Outcome category'),
                                         on_delete=models.SET_NULL)


class Outcome(models.Model):
    class Meta:
        verbose_name = _('Outcome')
        verbose_name_plural = _('Outcomes')

    user = models.ForeignKey(User, null=True, blank=False,
                             verbose_name=_('* Owner user'),
                             help_text=_('Set the user that is the owner'),
                             on_delete=models.SET_NULL)
    budget = models.ForeignKey(Budget, null=False, blank=False,
                               verbose_name=_('* Target budget'),
                               help_text=_('Choose target budget'),
                               on_delete=models.CASCADE)
    category = models.ForeignKey(OutcomeCategory, null=True, blank=False,
                                 verbose_name=_('* Category'),
                                 help_text=_('Set the category '
                                             'for this outcome'),
                                 on_delete=models.SET_NULL)
    value = models.DecimalField(_('* Value'), null=False, blank=False,
                                help_text=_('Set the amount of new outcome'),
                                default=0.0, decimal_places=2, max_digits=8)
    date = models.DateTimeField(_('* Creation date'), null=False, blank=True,
                                auto_now_add=True, auto_now=False,
                                help_text=_('Set the outcome date'))
    description = models.CharField(_('Description'), null=True, blank=True,
                                   help_text=_('Describe what is about '
                                               'this outcome'),
                                   max_length=254)
    is_planned = models.BooleanField(_('Is planned'), null=False, blank=True,
                                     help_text=_('Does it planned outcome?'),
                                     default=False)
    place = models.ForeignKey(OutcomePlace, null=True, blank=True,
                              verbose_name=_('Place'),
                              help_text=_('set the place for outcome'),
                              on_delete=models.SET_NULL)

    def __str__(self):
        return str(format_lazy('{value}: {category}',
                               value=self.value, category=self.category))


class Period(models.Model):
    class Meta:
        verbose_name = _('Period type')
        verbose_name_plural = _('Period types')

    YEAR = _('year')
    QUARTER = _('quarter')
    MONTH = _('month')
    WEEK = _('week')
    DAY = _('day')

    PERIOD_CHOICES = (
        (YEAR, _('year')),
        (QUARTER, _('quarter')),
        (MONTH, _('month')),
        (WEEK, _('week')),
        (DAY, _('day')),
    )

    period = models.CharField(_('* Period type'),
                              help_text='add one of predefined period type',
                              choices=PERIOD_CHOICES, default=MONTH,
                              max_length=20, unique=True)

    def __str__(self):
        return str(format_lazy('{period}', period=self.period))


class Profile(models.Model):
    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    # the value should't be translatable and should have relative url name
    INCOME = 'incomes'
    OUTCOME = 'outcomes'
    ADD_INCOME = 'add-income'
    ADD_OUTCOME = 'add-outcome'
    PROFILE = 'profile'

    START_PAGE_CHOICES = (
        (INCOME, 'incomes'),
        (OUTCOME, 'outcomes'),
        (ADD_INCOME, 'add-income'),
        (ADD_OUTCOME, 'add-outcome'),
        (PROFILE, 'profile'),
    )

    EN = 'en'
    UK = 'ek'
    RU = 'ru'

    LANGUAGE_CHOICES = (
        (EN, 'en'),
        (UK, 'uk'),
        (RU, 'ru'),
    )

    user = models.ForeignKey(User, null=True, blank=False,
                             verbose_name=_('* Target user'),
                             help_text=_('Set the target user'),
                             on_delete=models.CASCADE)
    start_page = models.CharField(_('* Your start page'),
                                  null=False, blank=False, max_length=50,
                                  help_text=_('choose your start page'),
                                  choices=START_PAGE_CHOICES,
                                  default=ADD_OUTCOME)
    default_budget = models.ForeignKey(Budget, null=True, blank=False,
                                       verbose_name=_('* Default user budget'),
                                       help_text=_('set your default budget'),
                                       on_delete=models.SET_NULL)
    default_income_category = models.ForeignKey(
        IncomeCategory, null=True, blank=False,
        verbose_name=_('* Default category for new income'),
        help_text=_('set default income category for your new income'),
        on_delete=models.SET_NULL
    )
    default_outcome_category = models.ForeignKey(
        OutcomeCategory, null=True, blank=False,
        verbose_name=_('* Default category for new outcome'),
        help_text=_('set default outcome category for your new outcome'),
        on_delete=models.SET_NULL
    )
    default_period = models.ForeignKey(
        Period, null=True, blank=False,
        verbose_name=_('* Default period'),
        help_text=_('set default period to calc your budget analytics'),
        on_delete=models.SET_NULL
    )
    language = models.CharField(_('* Language'),
                                null=False, blank=False, max_length=4,
                                help_text=_('choose your interface language'),
                                choices=LANGUAGE_CHOICES,
                                default=EN)


class BudgetRuleSet(models.Model):
    class Meta:
        verbose_name = _('budget rule set')
        verbose_name_plural = _('budget rule sets')

    income_read = models.BooleanField(_('Can read incomes'), default=True)
    income_write = models.BooleanField(_('Can change incomes'), default=True)
    income_add = models.BooleanField(_('Can add new incomes'), default=True)
    income_dell = models.BooleanField(_('Can delete incomes'), default=True)

    outcome_read = models.BooleanField(_('Can read outcomes'), default=True)
    outcome_write = models.BooleanField(_('Can change outcomes'), default=True)
    outcome_add = models.BooleanField(_('Can add new outcomes'), default=True)
    outcome_dell = models.BooleanField(_('Can delete outcomes'), default=True)

    income_category_read = models.BooleanField(_('Can read income category'), default=True)
    income_category_write = models.BooleanField(_('Can change income category'), default=True)
    income_category_add = models.BooleanField(_('Can add new income category'), default=True)
    income_category_dell = models.BooleanField(_('Can delete income category'), default=True)

    outcome_category_read = models.BooleanField(_('Can read outcome category'), default=True)
    outcome_category_write = models.BooleanField(_('Can change outcome category'), default=True)
    outcome_category_add = models.BooleanField(_('Can add new outcome category'), default=True)
    outcome_category_dell = models.BooleanField(_('Can delete outcome category'), default=True)

    outcome_place_read = models.BooleanField(_('Can read outcome places'), default=True)
    outcome_place_write = models.BooleanField(_('Can change outcome places'), default=True)
    outcome_place_add = models.BooleanField(_('Can add new outcome places'), default=True)
    outcome_place_dell = models.BooleanField(_('Can delete outcome places'), default=True)


class BudgetAccess(models.Model):
    class Meta:
        verbose_name = _('Budget access')
        verbose_name_plural = _('Budgets access')

    budget = models.ForeignKey(Budget, null=False, blank=False,
                               verbose_name=_('* Target budget'),
                               help_text=_('Choose target budget'),
                               on_delete=models.CASCADE)
    target_user = models.ForeignKey(
        User, null=False, blank=False, verbose_name=_('* Owner user'),
        help_text=_('Set the user that is the owner'),
        on_delete=models.CASCADE)
    rules = models.ForeignKey(BudgetRuleSet, null=False, blank=False,
                              verbose_name=_('* Set appropriate rule set'),
                              on_delete=models.PROTECT)

    # def __str__(self):
    #     return str(format_lazy('Access rules on budget {budget} for user: {user}',
    #                            self.budget, self.target_user))
