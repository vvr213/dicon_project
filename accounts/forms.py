from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="メールアドレス", required=True)
    nickname = forms.CharField(label="ニックネーム", required=False, max_length=30)

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("このメールアドレスは既に登録されています。")
        return email

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "nickname", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"].lower()
        user.username = email
        user.email = email
        user.first_name = self.cleaned_data.get("nickname", "")
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(AuthenticationForm):
    """認証はそのまま、見た目だけ email に寄せる"""
    username = forms.CharField(
        label="メールアドレス",
        widget=forms.TextInput(attrs={"autofocus": True, "placeholder": "example@example.com"})
    )
