from django.db import models
from django.conf import settings
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.conf import settings
from django.http.request import HttpRequest
from db import get_db_handle
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.sessions.backends.base import SessionBase
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
"""
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email
"""































"""
class Vacations(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    current_time = models.DateTimeField(auto_now_add=True)
    is_by_schedule = models.BooleanField(null=True)
    startdate = models.DateField()
    finishdate = models.DateField()
    duration = models.IntegerField(null=True)
    supervisor = models.CharField(max_length=30, blank=True)
    jun_hr = models.CharField(max_length=30, blank=True)
    head_hr = models.CharField(max_length=30, blank=True)
    director = models.CharField(max_length=30, blank=True)
    comments = models.CharField(max_length=100, blank=True)
"""

"""
class UserBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        print('auth')
        user_collection = get_db_handle()['users']
        user_data = user_collection.find_one({'email': username})
        if user_data:
            print(user_data)
            user = User(username=username)
            print(user)
            print(password)
            return user if password == user_data['password'] else None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # Add any additional fields you require

    USERNAME_FIELD = 'username'

    objects = MyUserManager()

    def __str__(self):
        return self.username


class SessionStore(SessionBase):
    def __init__(self, session_key=None):
        super().__init__(session_key)
        self.collection = get_db_handle()['sessions']

    def load(self):
        session_data = self.collection.find_one({'_id': self.session_key})
        if session_data:
            return session_data.get('session_data', {})
        return {}

    def create(self):
        self._session_key = self._get_new_session_key()
        return self.session_key

    def save(self, must_create=False):
        session_data = {
            '_id': self.session_key,
            'session_data': self._get_session(no_load=must_create),
            'expire_date': self.get_expiry_date(),
        }
        print('save')
        self.collection.replace_one({'_id': self.session_key}, session_data, upsert=True)

    def delete(self, session_key=None):
        self.collection.delete_one({'_id': session_key or self.session_key})

    def exists(self, session_key):
        return self.collection.find_one({'_id': session_key}) is not None
"""
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
"""