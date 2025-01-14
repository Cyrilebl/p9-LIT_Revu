from django import forms
from .models import Ticket, UserFollows
from authentication.models import User


class TicketForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Titre"}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Description"})
    )

    class Meta:
        model = Ticket
        exclude = ("user",)


class UserFollowsForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ["followed_user"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if not user.is_superuser:
            self.fields["followed_user"].queryset = User.objects.filter(
                is_superuser=False
            ).exclude(id=user.id)
        else:
            self.fields["followed_user"].queryset = User.objects.exclude(id=user.id)

        self.fields["followed_user"].empty_label = "Rechercher"
