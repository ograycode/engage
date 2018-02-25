from rest_framework import serializers
from root.models import Email, EmailGroup, EmailTemplate, Experiment, ProviderConfig

class EmailSerializer(serializers.HyperlinkedModelSerializer):
    email_group = serializers.PrimaryKeyRelatedField(queryset=EmailGroup.objects.all())
    provider = serializers.PrimaryKeyRelatedField(queryset=ProviderConfig.objects.all())
    template = serializers.PrimaryKeyRelatedField(queryset=EmailTemplate.objects.all(), required=False)
    experiment = serializers.PrimaryKeyRelatedField(queryset=Experiment.objects.all(), required=False)
    rendered = serializers.CharField(required=False)

    class Meta:
        model = Email
        fields = (
            'id',
            'to_emails',
            'from_email',
            'subject',
            'content_type',
            'data',
            'email_group',
            'provider',
            'sent_id',
            'template',
            'experiment',
            'rendered'
        )
