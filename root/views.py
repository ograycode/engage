from django.shortcuts import render as render_response
from django.views.generic.edit import FormView
from django.contrib.auth import login
from rest_framework import viewsets
from root.serializers import EmailSerializer
from root.email import render, send
from root.models import Email, EmailEvent
from root.forms import RegistrationForm

def index(request):
    return render_response(request, 'index.html', context={'user': request.user})

class SignUp(FormView):
    template_name = 'registration/sign_up.html'
    form_class = RegistrationForm
    success_url = '/'
    
    def form_valid(self, form):
        user, group = form.save()
        login(self.request, user)
        return super().form_valid(form)

class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all().order_by('-created_at')
    serializer_class = EmailSerializer

    def perform_create(self, serializer):
        email = serializer.save()
        needs_to_save = False
        if not email.rendered:
            template = email.email_group.default_template
            rendered = render(template.content, email.data)
            email.rendered = rendered
            email.template = template
            needs_to_save = True
        response = send(email)
        if response.status_code < 400:
            EmailEvent.objects.create(
                email=email,
                category='sent_to_provider',
                data={'status_code': response.status_code}
            )
        else:
            EmailEvent.objects.create(
                email=email,
                category='failed_to_send_to_provider',
                data={'status_code': response.status_code, raw: response.body}
            )
        if needs_to_save:
            email.save()
