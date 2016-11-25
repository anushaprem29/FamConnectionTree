from .models import *
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                label=_("Username"), error_messages={
            'invalid': _("This value must contain only letters, numbers and underscores.")})
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        label=_("Confirm Password"))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data


class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ('familyName','familyPicture','aboutFamily',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text','img','post_type',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name','phone','gender','picture','dob','familyName',)
        widgets = {
            'dob': forms.DateInput(attrs={'class': 'datepicker'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('msg_content','reciever',)
