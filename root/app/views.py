from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import Substr
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.urls import reverse
from root.forms import EmailGroupSetUpForm, ExperimentModelForm, EmailTemplateModelForm
from root.models import EmailGroup, Experiment, EmailTemplate

@login_required
def app_index(request):
    group_info = EmailGroup.objects.filter(
        group__users=request.user
    ).values(
        'id',
        'name',
        'default_template__id',
        'default_template__name'
    )
    for group in group_info:
        group['short_id'] = str(group['id'])[0:6]
    return render(
        request, 
        'app/index.html',
        context={
            'user': request.user,
            'sidebar_active': '/app/',
            'groups': group_info
        }
    )

@login_required
def email_group_detail(request, pk=None):
    group_info = EmailGroup.objects.filter(
        id=pk
    ).values(
        'id',
        'name',
        'default_template__name',
        'default_template__id'
    ).first()
    experiments = Experiment.objects.filter(
        email_group_id=pk
    ).order_by(
        'is_active',
        'start_time',
        'end_time',
        'id'
    ).values(
        'id',
        'name',
        'chance',
        'choice_a__id',
        'choice_a__name',
        'choice_b__id',
        'choice_b__name',
        'is_active',
        'start_time',
        'end_time'
    )
    templates = EmailTemplate.objects.filter(
        group_id=pk
    ).order_by(
        'created_at'
    ).values(
        'id',
        'name',
        'created_at',
        'updated_at'
    )
    setup_base_url = '{url}?email_group_id={id}'
    setup_link = setup_base_url.format(
        url=reverse('app:experiment-setup'),
        id=group_info['id']
    )
    template_setup_link = setup_base_url.format(
        url=reverse('app:template-setup'),
        id=group_info['id']
    )
    return render(
        request,
        'app/email_group_detail.html',
        context={
            'user': request.user,
            'group': group_info,
            'templates': templates,
            'experiments': experiments,
            'experiment_setup_link': setup_link,
            'template_setup_link': template_setup_link
        }
    )

class EmailGroupSetup(LoginRequiredMixin, FormView):
    template_name = 'app/email_group_setup.html'
    form_class = EmailGroupSetUpForm
    success_url = '/app/'

    def get_form(self):
        return self.form_class(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserFormMixin:
    def get_form(self):
        return self.form_class(self.request.user, **self.get_form_kwargs())

class ExperimentSetup(LoginRequiredMixin, UserFormMixin, CreateView):
    model = Experiment
    form_class = ExperimentModelForm
    template_name = 'app/experiment_setup.html'
    success_url = '/app/'

    def get_initial(self):
        initial = super().get_initial()
        if self.request.method == 'GET':
            initial.update({
                'email_group': self.request.GET.get('email_group_id')
            })
        return initial

class TemplateSetup(LoginRequiredMixin, UserFormMixin, CreateView):
    model = EmailTemplate
    form_class = EmailTemplateModelForm
    template_name = 'app/email_template_setup.html'
    success_url = '/app/'

    def get_initial(self):
        initial = super().get_initial()
        if self.request.method == 'GET':
            initial.update({
                'group': self.request.GET.get('email_group_id')
            })
        return initial

class TemplateEdit(LoginRequiredMixin, UserFormMixin, UpdateView):
    model = EmailTemplate
    form_class = EmailTemplateModelForm
    template_name = 'app/email_template_setup.html'
    success_url = '/app/'
