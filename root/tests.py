import copy
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from django.conf import settings
from model_mommy import mommy
from rest_framework.test import APIRequestFactory
from root.email.render import render
from root.models import EmailEvent
from root.forms import RegistrationForm, EmailGroupSetUpForm

class TestSendingAnEmail(APITestCase):

    def setUp(self):
        self.email_template = mommy.make('root.EmailTemplate')
        email_group = self.email_template.group
        email_group.default_template = self.email_template
        email_group.save()
        self.provider = mommy.make('root.ProviderConfig')

    def create_email_with_api(self):
        data = {
            'to_emails': ['to@test.com'],
            'from_email': 'from@test.com',
            'subject': 'this is the subject',
            'content_type': 'plaintext',
            'data': {
                'message': 'hello world'
            },
            'email_group': self.email_template.group.id,
            'provider': self.provider.id
        }
        response = self.client.post(
            reverse('api-email-list'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        return data, response

    def test_creating_an_email_to_send(self):
        data, response = self.create_email_with_api()
        # Fill in the data missing / not required
        data['template'] = self.email_template.id
        data['experiment'] = None
        data['rendered'] = render(self.email_template.content, data['data'])
        data['sent_id'] = ''
        # Delete the id
        del response.data['id']
        self.assertEqual(data, response.data)

    def test_creating_an_email_means_it_sends(self):
        data, response = self.create_email_with_api()
        event = EmailEvent.objects.get(email__id=response.data['id'])
        self.assertEqual(event.category, 'sent_to_provider')

class TestRegistrestionForm(TestCase):

    def setUp(self):
        txt = 'test123'
        self.valid_data = {
            'first_name': txt,
            'last_name': txt,
            'email': 'test@test.com',
            'username': txt,
            'password': txt,
            'group': txt
        }

    def create_form_assert_valid(self):
        form = RegistrationForm(self.valid_data)
        self.assertTrue(form.is_valid())
        return form

    def test_creating_a_user(self):
        form = self.create_form_assert_valid()
        user = form.create_user()
        self.assertIsNotNone(user.id)

    def test_creating_a_group_with_user(self):
        form = self.create_form_assert_valid()
        user = form.create_user()
        group = form.create_group(user)
        self.assertIsNotNone(user.id)
        self.assertEqual(group.users.first(), user)

    def test_invalid_data(self):
        for key, value in self.valid_data.items():
            data = copy.deepcopy(self.valid_data)
            data[key] = None
            form = RegistrationForm(data)
            self.assertFalse(form.is_valid())

class TestEmailGroupSetUpForm(TestCase):

    def setUp(self):
        user_group = mommy.make('root.UserGroup')
        self.user = mommy.make(settings.AUTH_USER_MODEL)
        user_group.users.add(self.user)
        self.valid_data = {
            'user_group': str(user_group.id),
            'group_name': 'test group name',
            'content': 'hello {{world}}',
            'content_type': 'text/plain',
            'preview_data': "{'content': 'preview'}",
            'name': 'test'
        }

    def create_form_assert_valid(self):
        form = EmailGroupSetUpForm(self.user, self.valid_data)
        self.assertTrue(form.is_valid())
        return form

    def test_creating_an_email_group(self):
        form = self.create_form_assert_valid()
        group = form.create_email_group()
        self.assertIsNotNone(group.id)
        self.assertEqual(
            str(group.group.id),
            self.valid_data['user_group']
        )
        self.assertEqual(group.name, self.valid_data['group_name'])

    def test_creating_an_email_group_with_template(self):
        form = self.create_form_assert_valid()
        group = form.create_email_group()
        template = form.create_template(group)
        self.assertEqual(template.group, group)
        self.assertEqual(template.content, self.valid_data['content'])
        self.assertEqual(
            template.content_type,
            self.valid_data['content_type']
        )
