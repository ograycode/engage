from django.forms import *
from django.forms import widgets


class BootstrapMixin:
    def __init__(self, *args, **kwargs):
        placeholder = kwargs.pop('placeholder', '')
        if not 'widget' in kwargs:
            kwargs['widget'] = self.widget(
                attrs={
                    'class': 'form-control',
                    'placeholder': placeholder
                }
            )
        return super().__init__(*args, **kwargs)

class CharField(BootstrapMixin, CharField):
    pass

class EmailField(BootstrapMixin, EmailField):
    pass

class ChoiceField(BootstrapMixin, ChoiceField):
    pass

class IntegerField(BootstrapMixin, IntegerField):
    pass

class DateTimeField(BootstrapMixin, DateTimeField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = self.widget(
            attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }
        )
        return super().__init__(*args, **kwargs)

class BooleanField(BootstrapMixin, BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = self.widget(
            attrs={
                'class': 'form-check-input'
            }
        )
        return super().__init__(*args, **kwargs)

class ModelChoiceField(BootstrapMixin, ModelChoiceField):
    pass
