from os import truncate
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from django.utils import timezone


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, firstname, lastname, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, firstname, lastname, password, **other_fields)

    def create_user(self, email, firstname, lastname, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, firstname=firstname,
                          lastname=lastname, **other_fields)
        user.set_password(password)
        user.save()
        return user


class PhisUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    firstname = models.CharField(max_length=150, blank=True)
    lastname = models.CharField(max_length=150, blank=True)
    auth_user_id = models.CharField(max_length=150, blank=True)
    user_role = models.CharField(max_length=2, blank=True)
    startDate = models.DateTimeField(default=timezone.now)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    def __str__(self):
        return self.email


class Microservice(models.Model):
    microserviceName = models.CharField(max_length=200)
    microserviceStatus = models.CharField(max_length=200, default='active', editable=False)
    microserviceUpdated = models.DateTimeField(auto_now=True)
    microserviceCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.microserviceName

    class Meta:
        ordering = ['-id']


class Menu(models.Model):
    microservice = models.ForeignKey(Microservice, on_delete=models.CASCADE)
    user = models.ForeignKey(PhisUser, on_delete=models.CASCADE)
    menuname = models.CharField(max_length=200)
    comment = models.TextField(max_length=400)
    menustatus = models.CharField(max_length=200, default='active', editable=False)
    menuupdated = models.DateTimeField(auto_now=True)
    menucreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.menuname

    class Meta:
        ordering = ['-id']


class Submenu(models.Model):
    user = models.ForeignKey(PhisUser, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    submenuname = models.CharField(max_length=200)
    submenuroute = models.CharField(max_length=300)
    submenudescription = models.CharField(max_length=200)
    comment = models.TextField(max_length=400)
    submenustatus = models.CharField(max_length=200, default='active', editable=False)
    submenuupdated = models.DateTimeField(auto_now=True)
    submenucreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.submenuname

    class Meta:
        ordering = ['-id']


class Post(models.Model):
    auth_user_id = models.CharField(max_length=150, blank=True)
    content_post_id = models.CharField(max_length=150, blank=True)
    post_title = models.CharField(max_length=200)
    post_content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']

class AuthorApplication(models.Model):
    PENDING = "P"
    DECLINED = "D"
    APPROVED = "A"

    # Author application choices
    AA_STATUS = [
        (PENDING, 'pending'),
        (DECLINED, 'declined'),
        (APPROVED, 'approved')
    ]
    email = models.EmailField(unique=True)
    google_scholar = models.URLField(max_length=200, null=True, unique=True)
    research_gate = models.URLField(max_length=200, null=True, unique=True)
    scopus = models.URLField(max_length=200, null=True, unique=True)
    pub_med = models.URLField(max_length=200, null=True, unique=True)
    capic_status = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=2, choices=AA_STATUS, default=PENDING)
    applied_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)

class Followers(models.Model):
    author_email = models.EmailField(_('email address'), unique=True)
    followers = models.ManyToManyField(PhisUser)
# class Role(models.Model):
#     pass
#
#
# class Criteria(models.Model):
#     pass
