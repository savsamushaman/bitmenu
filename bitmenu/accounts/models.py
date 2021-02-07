from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class CustomUser(AbstractUser):
    objects = CustomUserManager()

    slug = models.SlugField(blank=True, null=False)
    email = models.EmailField(unique=True, blank=False)

