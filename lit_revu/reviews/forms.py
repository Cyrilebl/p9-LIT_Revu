from django import forms
from .models import Ticket, Review, UserFollows
from authentication.models import User


class TicketForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Titre"}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Description"})
    )

    class Meta:
        model = Ticket
        exclude = ("user",)


class ReviewForm(forms.ModelForm):
    headline = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Titre"}))
    body = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Description"}))
    rating = forms.ChoiceField(
        choices=[("", "Note sur 5")] + [(i, str(i)) for i in range(6)],
        widget=forms.Select(),
        label="Note",
    )

    class Meta:
        model = Review
        exclude = ("user", "ticket")


class UserFollowsForm(forms.Form):
    followed_user = forms.CharField(
        label="Rechercher un utilisateur",
        widget=forms.TextInput(attrs={"placeholder": "Saisissez un nom d'utilisateur"}),
        required=True,
    )

    class Meta:
        model = UserFollows
        fields = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_followed_user(self):
        username = self.cleaned_data.get("followed_user")

        if not username:
            raise forms.ValidationError("Veuillez saisir un nom d'utilisateur valide.")

        # Filtrer les utilisateurs en fonction des critères
        try:
            if self.user and not self.user.is_superuser:
                followed_user = User.objects.filter(is_superuser=False).get(
                    username=username
                )
            else:
                followed_user = User.objects.exclude(id=self.user.id).get(
                    username=username
                )
        except User.DoesNotExist:
            raise forms.ValidationError("Cet utilisateur n'existe pas.")

        return followed_user
