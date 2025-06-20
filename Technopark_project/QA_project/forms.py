from django.contrib.auth.models import User
from .models import Profile, Question, Answer, Tag
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class AskForm(forms.ModelForm):
    tags = forms.CharField(
        help_text="Enter up to 5 tags separated by commas",
        widget=forms.TextInput(attrs={'placeholder': 'tag1, tag2, tag3'})
    )

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        tag_names = [name.strip() for name in tags.split(',') if name.strip()]

        if len(tag_names) > 5:
            raise forms.ValidationError("You can't add more than 5 tags.")

        for tag in tag_names:
            if len(tag) > 50:
                raise forms.ValidationError(f"Tag '{tag}' is too long (max 50 characters).")
            if not tag.isalnum():
                raise forms.ValidationError(f"Tag '{tag}' contains invalid characters. Use letters and numbers only.")

        return tags

    def save(self, author):
        question = super().save(commit=False)
        question.author = author
        question.save()

        tag_names = [name.strip() for name in self.cleaned_data['tags'].split(',') if name.strip()]
        tag_names = tag_names[:5]
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name.lower())
            question.tags.add(tag)

        return question

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput, label='Repeat Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                nickname=user.username,
                user_email=user.email
            )
        return user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")

        if password and repeat_password and password != repeat_password:
            self.add_error('repeat_password', "Пароли не совпадают")

        return cleaned_data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'avatar', 'user_email']
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'user_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            profile.user = self.user
        if commit:
            profile.save()
        return profile