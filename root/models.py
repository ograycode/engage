import uuid
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserGroup(BaseModel):
    name = models.TextField()
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    apikey = models.UUIDField(default=uuid.uuid4)

class ProviderConfig(BaseModel):
    name = models.TextField()
    apikey = models.TextField()
    group = models.ForeignKey(UserGroup)
    service = models.TextField(choices=(('sendgrid', 'Sendgrid'),))

class EmailGroup(BaseModel):
    name = models.TextField()
    group = models.ForeignKey(UserGroup)
    default_template = models.ForeignKey('EmailTemplate', null=True)

class EmailTemplate(BaseModel):
    name = models.TextField()
    group = models.ForeignKey('EmailGroup')
    subject = models.TextField()
    content = models.TextField()
    content_type = models.TextField()
    preview_data = JSONField(default={'content': 'hello world'})

    def __str__(self):
        return self.name

class Experiment(BaseModel):
    name = models.TextField()
    chance = models.IntegerField()
    choice_a = models.ForeignKey(
        EmailTemplate,
        related_name='primary_experiment_choice'
    )
    choice_b = models.ForeignKey(
        EmailTemplate,
        null=True,
        related_name='secondary_experiment_choice'
    )
    email_group = models.ForeignKey(EmailGroup)
    is_active = models.BooleanField()
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

class Email(BaseModel):
    # Provider information
    sent_id = models.TextField(blank=True)
    provider = models.ForeignKey(ProviderConfig)
    # Email information
    data = JSONField(blank=True)
    rendered = models.TextField()
    to_emails = ArrayField(models.TextField())
    from_email = models.TextField()
    subject = models.TextField()
    content_type = models.TextField()
    # Meta information
    template = models.ForeignKey(EmailTemplate, null=True)
    experiment = models.ForeignKey(Experiment, null=True)
    email_group = models.ForeignKey(EmailGroup)

class EmailEvent(BaseModel):
    email = models.ForeignKey(Email)
    category = models.TextField()
    data = JSONField()
