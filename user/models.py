from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # email = None

    class Meta:
        db_table = 'User'



class UserPhoneNo():
    pass


class UserAddress():
    pass