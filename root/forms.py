from django.contrib.auth import get_user_model
from django.forms import widgets
from root import forms_override as forms
from root.models import UserGroup, EmailTemplate, EmailGroup, Experiment

INITIAL_EMAIL_TEMPLATE = """<html>
    <body>
        <h1>{{content}}</h1>
    </body>
</html>
"""
class RegistrationForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField(
        min_length=5,
        widget=widgets.PasswordInput(attrs={'class': 'form-control'})
    )
    group = forms.CharField()

    def create_user(self):
        data = self.cleaned_data
        return get_user_model().objects.create_user(
            data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        

    def create_group(self, user):
        group = UserGroup.objects.create(
            name=self.cleaned_data['group']
        )
        group.users.add(user)
        return group

    def save(self):
        user = self.create_user()
        group = self.create_group(user)
        return user, group

class EmailGroupSetUpForm(forms.Form):
    user_group = forms.ChoiceField()
    group_name = forms.CharField()
    name = forms.CharField()
    content = forms.CharField(
        initial=INITIAL_EMAIL_TEMPLATE,
        widget=widgets.Textarea(attrs={'class': 'form-control'})
    )
    content_type = forms.ChoiceField(
        choices=(
            ('text/html; charset=UTF-8', 'text/html; charset=UTF-8'),
            ('text/plain', 'text/plain')
        )
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_group'] = forms.ChoiceField(
            choices=UserGroup.objects.filter(users=user).values_list('id', 'name')
        )

    def create_email_group(self):
        return EmailGroup.objects.create(
            name=self.cleaned_data['group_name'],
            group_id=self.cleaned_data['user_group'],
        )

    def create_template(self, group):
        return EmailTemplate.objects.create(
            group=group,
            name=self.cleaned_data['name'],
            content=self.cleaned_data['content'],
            content_type=self.cleaned_data['content_type']
        )

    def save(self):
        group = self.create_email_group()
        template = self.create_template(group)
        return group, template

class ExperimentModelForm(forms.ModelForm):
    name = forms.CharField()
    chance = forms.IntegerField(min_value=0, max_value=100, initial=50)
    start_time = forms.DateTimeField(required=False)
    end_time = forms.DateTimeField(required=False)
    is_active = forms.BooleanField(required=False)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        query = EmailTemplate.objects.filter(group__group__users__in=[user])
        self.fields['choice_a'] = forms.ModelChoiceField(
            queryset=query
        )
        self.fields['choice_b'] = forms.ModelChoiceField(
            queryset=query
        )
        self.fields['email_group'] = forms.ModelChoiceField(
            queryset=EmailGroup.objects.filter(group__users__in=[user]),
            widget=forms.HiddenInput()
        )
    
    class Meta:
        model = Experiment
        fields = [
            'name', 'chance',
            'choice_a', 'choice_b',
            'start_time', 'end_time', 
            'is_active', 'email_group'
        ]

class EmailTemplateModelForm(forms.ModelForm):
    name = forms.CharField()
    subject = forms.CharField(initial='Subjects are also a template: {{content}}')
    content = forms.CharField(
        initial=INITIAL_EMAIL_TEMPLATE,
        widget=widgets.Textarea(attrs={'class': 'form-control'})
    )
    content_type = forms.ChoiceField(
        choices=(
            ('text/html; charset=UTF-8', 'text/html; charset=UTF-8'),
            ('text/plain', 'text/plain')
        )
    )
    preview_data = forms.CharField(
        widget=widgets.Textarea(attrs={'class': 'form-control'}),
        initial='{"content": "hello-world"}'
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'] = forms.ModelChoiceField(
            queryset=EmailGroup.objects.filter(group__users__in=[user]),
            widget=forms.HiddenInput()
        )

    class Meta:
        model = EmailTemplate
        fields = [
            'name', 'group',
            'content', 'content_type',
            'preview_data'
        ]
