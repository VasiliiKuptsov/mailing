from django import forms
from .models import Mailing, Message, AttemptMailing


class OwnerMailingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["message"].queryset = Message.objects.filter(owner=user)

    class Meta:
        model = Mailing
        fields = ["message", "recipient"]


class ManagerMailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["is_active"]


class OwnerAttemptForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["mailing"].queryset = Mailing.objects.filter(owner=user)

    class Meta:
        model = AttemptMailing
        fields = ["mailing"]