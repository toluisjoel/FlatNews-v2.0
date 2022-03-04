from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.CharField(max_length= 800, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    GENDER_CHOICES = ('male', 'male'), ('female', 'female'), ('other', 'other')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='female')
    profile_picture = models.ImageField(default='users/default_profile_photo.svg', upload_to='users/%Y/%m/%d/')
    country = CountryField(blank=True)

    def __str__(self):
        return f'Profile for {self.user.username}'
