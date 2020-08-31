from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.urls import reverse
from allauth.account.forms import SignupForm
from django.template.defaultfilters import slugify


class Story(models.Model):
    """
   Study Schema
    """
    title = models.CharField(max_length=100)
    story = models.TextField()
    publish = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)


class Mcq(models.Model):
    """
   Multiple Choice Questions
    """
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    question = models.CharField(max_length=400)
    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    option_c = models.CharField(max_length=100)
    option_d = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)

    def __str__(self):
        return str(self.question[:100])


class Profile(models.Model):
    """
    User Profile
    """
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    total_points = models.IntegerField(blank=True, null=True)
    assessed = models.BooleanField(default=False)
    malpractise = models.BooleanField(default=False)
    url = models.SlugField(blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        if self.user:
            self.url = slugify(str(self.user))
            super(Profile, self).save(*args, **kwargs)


class CustomSignupForm(SignupForm):
    """
    Here we extend the Signup form to add first and last Nname fields
    and also Create Profile with the Data on SignUp
    """
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = '__all__'

    def save(self, request):
        request.user.first_name = self.cleaned_data['first_name']
        request.user.last_name = self.cleaned_data['last_name']
        request.user = super(CustomSignupForm, self).save(request)
        request.user.save()
        profile, created = Profile.objects.get_or_create(
            user=request.user,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
        )
        profile.save()
        return request.user
