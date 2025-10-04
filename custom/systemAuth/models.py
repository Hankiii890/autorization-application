from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.validators import EmailValidator 
from django.utils.translation import gettext_lazy as _
from django.utils import timezone 


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, commit=True):
        if not email:
            raise ValueError(_("email is a required velue"))
        if not password:
            raise ValueError(_("enter your passwor!"))
   
        # Создание объекта пользователя - шаблон"чик
        user = self.model(email = self.normalize_email(email),
                          first_name=first_name, 
                          last_name=last_name,
                          )
        
        user.set_password(password) 
        if commit:
            user.save(using=self._db)
        return user 


    def create_admin(self, email, password, first_name):
        '''Тут происходит создание админа'''
        user_admin = self.create_user(email, 
                                password=password,
                                first_name=first_name,
                                commit=False)    # не сохраняем сразу в бд
        user_admin.is_staff = True 
        user_admin.is_superuser = True 
        user_admin.save(using=self._db)
        return user_admin 
    
class User(AbstractUser, PermissionsMixin):
    """
    AbstratcUser - базовая функциональность аутентификации 
    PermissionsMixin - система разрешений и групп !
    """

    email = models.EmailField(verbose_name=_('email addres'), max_length=255, unique=True) 
    # password предоставляется AbstractUser 
    first_name = models.CharField(_("user name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=30, help_text="Фамилия пользователя")
    is_active = models.BooleanField(_("active"), default=True, help_text="Надо снять галочку вместо удаления при удалении акка")    
    is_staff = models.BooleanField(_("staff status"), default=False)    # То что обычный бзер не сможет зайти в админку!
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)  # Дата и время создания "пользователя"!

objects = UserManager()  # Объект создания и ответов для пользователей

USERNAME_FIED = 'email'
REQUIRED_FIELDS = ['first_name']    # обязательно при создании админа  

def __str__(self):
    return f"{self.email} ({self.get_full_name()})"

def get_full_name(self):
    return f"{self.first_name} {self.last_name}".strip()




